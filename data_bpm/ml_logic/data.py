import pandas as pd
import os.path as Path
from colorama import Fore, Style
from data_bpm import params
import numpy as np
import string as str
import unicodedata
from io import BytesIO

from google.cloud import bigquery
from google.cloud import storage

def clean_data(data_events_ppl, data_scraped):
    '''
    Clean the data, merge the three files and returns two datframes
    1. Data for model
    2. Data for dashboard
    MVP: merging only the first two files
    '''
    # Clean data_events_ppl
    # breakpoint()
    if len(data_events_ppl) == 0:
        print(Fore.RED + "\nEvents and ppl data is empty!" + Style.RESET_ALL)
        return (None,None)
    if len(data_scraped) == 0:
        print(Fore.RED + "\nScraped data is empty!" + Style.RESET_ALL)
        return (None,None)
    # breakpoint()
    data_events_ppl["First Name"] = data_events_ppl["First Name"].apply(process_name)
    data_events_ppl["Surname"] = data_events_ppl["Surname"].apply(process_name)
    data_events_ppl["fullName"] = data_events_ppl["First Name"] + ' ' + data_events_ppl["Surname"]

    data_events_ppl['Email'] = data_events_ppl['Email'].fillna('').str.lower()
    data_events_ppl['Company'] = data_events_ppl["Company"].apply(process_name)

    # Create DF with unique IDs------------------------------

    # Define custom function to get the first non-null value
    def first_non_null(series):
        return series.dropna().iloc[0] if not series.dropna().empty else np.nan

    # Columns where you want to apply the first_non_null function
    columns_to_agg = ['First Name',
                      'Surname',
                      'Email',
                      'Company',
                      'Your Job Position',
                      'Choose your role',
                      'Choose your role.1',
                      'Seniority'
                      ]

    # Create a dictionary to specify aggregation functions for each column

    def calculate_attended(group):

        # Get the last event for the group
        last_event = group.iloc[-1]

        #breakpoint()

        # Check if the last event's Attendee Status is "Checked In"
        if last_event == 'Checked In':
            return 1
        else:
            return 0


    agg_dict = {'Event': 'count', 'Attendee Status': calculate_attended }
    agg_dict.update({column: first_non_null for column in columns_to_agg})
    # Group by UserID and apply the calculate_attended function

    # Group by 'fullName' and apply aggregation
    unique_attendees = data_events_ppl.groupby(by='fullName', as_index=False).agg(agg_dict)
    unique_attendees["numEvents"] = unique_attendees.Event

    # Index in this table is now the user ID
    unique_attendees['UserID'] = unique_attendees.index

    # we have numEvents now instead
    unique_attendees = unique_attendees.drop(labels='Event',axis=1)
    unique_attendees["Company"] = unique_attendees["Company"].apply(process_name)

    # Clean data_scraped
    data_scraped.lastName = data_scraped.lastName.apply(process_name)
    data_scraped.firstName = data_scraped.firstName.apply(process_name)
    data_scraped.fullName = data_scraped.firstName + ' ' + data_scraped.lastName
    data_scraped.dropna(subset=['url'])

    data_scraped['email'] = data_scraped['email'].fillna('').str.lower()
    data_scraped['company'] = data_scraped['company'].fillna('').str.lower().str.strip()

    data_scraped['UserID'] = float('nan')
    data_scraped['Attendance'] = 0
    # Iterate through each row in the ids DataFrame
    for j, row_ids in unique_attendees.iterrows():
        # Iterate through each row in the scraped DataFrame
        for index_scraped, row_scraped in data_scraped.iterrows():
            # Check if the rows match using the custom matching function
            if custom_user_matching(row_scraped, row_ids):
                # If a match is found, add the userID from the ids DataFrame to the scraped DataFrame
                data_scraped.at[index_scraped, 'UserID'] = row_ids['UserID']
                data_scraped.at[index_scraped, 'Attendance'] = row_ids['Attendee Status']
                break
    # Drop rows with NaN values in the 'UserID' column
    data_merged = data_scraped.dropna(subset=['UserID'])

    columns_to_drop = ['url', 'title', 'linkedinProfileUrl', 'email', 'linkedinProfile', 'firstName', 'lastName',
                   'fullName', 'connectionDegree', 'timestamp', 'subscribers', 'mutualConnectionsText', 'imgUrl', 'website', 'mail',
                   'profileId', 'baseUrl', 'connectionDegree', 'vmid', 'userId', 'linkedinSalesNavigatorUrl', 'connectionsCount', 'connectionsUrl',
                   'mutualConnectionsUrl','companyUrl','companyUrl2','schoolUrl','schoolUrl2','jobDateRange2',
                   'connectedOn', 'phoneNumber', 'partialScreenshot', 'facebookUrl', 'website', 'error']

    # Drop columns from the merged
    data_merged.drop(columns=columns_to_drop, inplace=True)
    data_merged.set_index('UserID', inplace=True)

    # Dropping a particular row as for a invalid format for jobDuration "Less than 1 year"
    # To do a more sophisticate function to handle these type of data in cleaning
    # data_merged.drop(509, inplace=True)

    # create the data frame for the analytics-----------------------------------------

    data_analytics = data_events_ppl.merge(unique_attendees[["UserID","fullName"]], how = 'right',on = "fullName")
    data_analytics.drop(labels = ['First Name','Surname','Email','fullName'], axis=1, inplace=True)

    # Merge the two DataFrames on 'UserID'
    merged_df = data_analytics.merge(data_merged[['company','jobTitle','jobTitle2']], how='left', left_on='UserID', right_index=True)

    # Replace suspicious and empty strings in the Company name with NaNs
    to_replace_list = ['','none','xxx','-','tbd','123','n','na','x','--']
    merged_df['Company'].replace(to_replace_list, pd.NA, inplace=True)

    # Update 'Company' with values from 'company' where 'Company' is NaN
    merged_df['Company'].fillna(merged_df['company'], inplace=True)
    data_analytics['Company'] = merged_df['Company']

    # Update 'Choose your role' with values from 'jobTitle' where 'Choose your role' is NaN
    merged_df['Choose your role'].fillna(merged_df['jobTitle'], inplace=True)
    data_analytics['Choose your role'] = merged_df['Choose your role']

    # Update 'Choose your role.1' with values from 'jobTitle2' where 'Choose your role.1' is NaN
    merged_df['Choose your role.1'].fillna(merged_df['jobTitle2'], inplace=True)
    data_analytics['Choose your role.1'] = merged_df['Choose your role.1']

    data_analytics.set_index('UserID', inplace=True)

    return (data_merged, data_analytics)

def get_data():

    data_events_ppl = pd.DataFrame()
    data_scraped = pd.DataFrame()
    data_events_series = pd.DataFrame()

    # Get Data from Goggle Cloud Storage
    if params.DATA_TARGET == 'gcs':
        data_events_ppl, data_scraped = get_data_from_gcs()
        print(f"✅ All 2 Data files loaded from GCS")

    elif params.DATA_TARGET == 'local':
        print(Fore.BLUE + "\nLoad data from local CSV..." + Style.RESET_ALL)

        # Get Local Data
        data_events_ppl = pd.read_csv(Path.join("raw_data", params.RAW_FILE_EVENT))
        data_scraped = pd.read_csv(Path.join("raw_data", params.RAW_FILE_SCRAPPED))

    else:
        print(Fore.RED + "\nMODEL_TARGET not set, exiting" + Style.RESET_ALL)
        return(None,None)

    return clean_data(data_events_ppl, data_scraped)

def load_data_to_bq(
        data: pd.DataFrame,
        gcp_project:str,
        bq_dataset:str,
        table: str,
        truncate: bool
    ) -> None:

    """
    - Save the DataFrame to BigQuery
    - Empty the table beforehand if `truncate` is True, append otherwise
    """
    pass


def first_non_null(series):
    '''
    Utility function to get the first non-null value
    '''
    return series.dropna().iloc[0] if not series.dropna().empty else None


def process_name(name):
    '''
    Utility function to process names
    '''
    # replace NaN with an empty string
    if pd.isna(name):
        return ''
    # strip dots and spaces and get only the longest/first word
    words = name.lower().strip(" .").split()

    # Initialize variables to keep track of the longest word
    longest_word = ''
    longest_length = 0

    # Iterate through each word
    for word in words:
        # If the current word is longer than the longest word found so far, or if it's equal in length but appears earlier
        if len(word) > longest_length or (len(word) == longest_length and words.index(word) < words.index(longest_word)):
            longest_word = word
            longest_length = len(word)

    # Normalize the string to decomposed Unicode form
    normalized_s = unicodedata.normalize('NFD', longest_word)

    # Remove non-spacing marks (special characters)
    stripped_s = ''.join(c for c in normalized_s if unicodedata.category(c) != 'Mn')

    return stripped_s

def custom_user_matching(row_scraped, row_ids):
    '''
    Utility function to match scraped data with UserIDs
    '''
    if row_scraped['fullName'] == row_ids['fullName']:
        return True

    # Compare the emails
    if row_scraped['email'] == row_ids['Email'] :
        return True

    if not pd.isna(row_scraped['company']):
        # Compare first or last name match AND the company match
        if (row_scraped['lastName'] in row_ids['Surname']) and ( not pd.isna(row_scraped['lastName'])) :
            if (row_ids['Company'] in row_scraped['company'].lower()) and ( len(row_ids['Company']) != 0):
                return True
        if (row_scraped['firstName'] in row_ids['First Name']) and ( not pd.isna(row_scraped['firstName'])) :
            if (row_ids['Company'] in row_scraped['company'].lower()) and ( len(row_ids['Company']) != 0):
                return True


def get_data_from_gcs():
    '''
    This method will read the latest csv data from google cloud storage |
    Data files will be uploaded manually from the stakeholder
    '''
    print(Fore.BLUE + f"\nLoad latest data files from GCS..." + Style.RESET_ALL)

    bucket_name = params.BUCKET_NAME
    gsfile_path_events_ppl = f'gs://{bucket_name}/{params.RAW_FILE_EVENT}'
    gsfile_path_scrapped = f'gs://{bucket_name}/{params.RAW_FILE_SCRAPPED}'

    try:
        data_events_ppl = pd.read_csv(gsfile_path_events_ppl)
        data_scraped = pd.read_csv(gsfile_path_scrapped)

        print("✅ Latest files loaded from cloud storage")

        return (True, clean_data(data_events_ppl, data_scraped))
    except FileNotFoundError as e:
        print(f"\n❌ No files found in GCS bucket {bucket_name}")
        # print(f"File {gsfile_path_events_ppl} not found in bucket {bucket_name}")
        return (False, e)

def save_data_to_gcs(
        data_ml: pd.DataFrame,
        data_analytics: pd.DataFrame
    ):

    '''
    Save the cleaned version of data in google cloud storage to nake it available to Dashboard
    '''
    client = storage.Client()
    bucket = client.bucket(params.BUCKET_NAME)

    try:
        # Convert DataFrame to CSV format in memory
        csv_buffer_ml = BytesIO()
        data_ml.to_csv(csv_buffer_ml, index=False)

        csv_buffer_analysis = BytesIO()
        data_analytics.to_csv(csv_buffer_analysis, index=False)

        # Specify the bucket name and CSV file path in GCS | Used in printing only
        gcsfile_name_ml = f'gs://{params.BUCKET_NAME}/{params.CLEANED_FILE_ML}'
        gcsfile_name_analytics = f'gs://{params.BUCKET_NAME}/{params.CLEANED_FILE_ANALYTICS}'

        # Create a Blob object and upload the CSV data
        blob_ml = bucket.blob(params.CLEANED_FILE_ML)
        blob_ml.upload_from_string(csv_buffer_ml.getvalue(), content_type='text/csv')

        blob_analysis = bucket.blob(params.CLEANED_FILE_ANALYTICS)
        blob_analysis.upload_from_string(csv_buffer_analysis.getvalue(), content_type='text/csv')

        print(f"DataFrame successfully written to '{gcsfile_name_ml}'")
        print(f"DataFrame successfully written to '{gcsfile_name_analytics}'")

        return True, "OK"

    except Exception as e:
        print(f"\n❌ No files saved in GCS bucket {bucket}")

        return False, e
