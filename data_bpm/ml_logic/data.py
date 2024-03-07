import pandas as pd
import os.path as Path
from colorama import Fore, Style
from google.cloud import bigquery
from data_bpm import params
import numpy as np
import string as str
import unicodedata

def clean_data(data_events_ppl,data_scraped):
    '''
    Clean the data, merge the three files and returns a single datframe
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
    agg_dict = {'Event': 'count'}
    agg_dict.update({column: first_non_null for column in columns_to_agg})

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
    # Iterate through each row in the ids DataFrame
    for j, row_ids in unique_attendees.iterrows():
        # Iterate through each row in the scraped DataFrame
        for index_scraped, row_scraped in data_scraped.iterrows():
            # Check if the rows match using the custom matching function
            if custom_user_matching(row_scraped, row_ids):
                # If a match is found, add the userID from the ids DataFrame to the scraped DataFrame
                data_scraped.at[index_scraped, 'UserID'] = row_ids['UserID']
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

    return (data_merged,data_analytics)

def get_data():

    data_events_ppl = pd.DataFrame()
    data_scraped = pd.DataFrame()
    data_events_series = pd.DataFrame()

    # Get Data from Goggle Cloud BigQuery
    if params.MODEL_TARGET == 'gcs':
        """
        Retrieve `query` data from BigQuery, or from `cache_path` if the file exists
        Store at `cache_path` if retrieved from BigQuery for future use
        """
        print(Fore.BLUE + "\nLoading raw_all data from BigQuery server..." + Style.RESET_ALL)
        query_1 = """SELECT {",".join(COLUMN_NAMES_RAW)}
        FROM {GCP_PROJECT}.{BQ_DATASET}.raw_all
        """
        client = bigquery.Client(project=params.GCP_PROJECT)
        query_1_job = client.query(query_1)
        result = query_1_job.result()
        data_events_ppl = result.to_dataframe()

        print(f"raw_all Data loaded, with shape {data_events_ppl.shape}")
        ##############

        print(Fore.BLUE + "\nLoading raw_scrapped data from BigQuery server..." + Style.RESET_ALL)
        query_2 = """SELECT {",".join(COLUMN_NAMES_RAW)}
        FROM {GCP_PROJECT}.{BQ_DATASET}.raw_scrapped
        """
        query_2_job = client.query(query_2)
        result_2 = query_2_job.result()
        data_scraped = result_2.to_dataframe()

        print(f"raw_scrapped Data loaded, with shape {data_scraped.shape}")
        ##############

        print(Fore.BLUE + "\nLoading raw_events data from BigQuery server..." + Style.RESET_ALL)
        query_3 = """SELECT {",".join(COLUMN_NAMES_RAW)}
        FROM {GCP_PROJECT}.{BQ_DATASET}.raw_events
        """
        query_3_job = client.query(query_3)
        result_3 = query_3_job.result()
        data_events_series = result_3.to_dataframe()
        print(f"raw_scrapped Data loaded, with shape {data_events_series.shape}")


        print(f"✅ All 3 Data files loaded")


    elif params.MODEL_TARGET == 'local':
        print(Fore.BLUE + "\nLoad data from local CSV..." + Style.RESET_ALL)

        # Get Local Data'
        data_events_ppl = pd.read_csv(Path.join("raw_data", "240304 BPM Events list people  - ALL __.csv"))
        data_scraped = pd.read_csv(Path.join("raw_data", "result.csv"))
        # data_events_series = pd.read_csv(Path.join("..","raw_data", "BPM Events list people.csv"))
    else:
        print(Fore.RED + "\nMODEL_TARGET not set, exiting" + Style.RESET_ALL)
        return(None,None)

    # Clean Data
#     clean_data()
#     return dict({'data_all' : data_events_ppl,
#                  'data_dcrapped' : data_scraped,
#                  'data_events' : data_events_series
#     })

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
