import pandas as pd
import os.path as Path
import numpy as np
import string as str
import unicodedata

def clean_data(data_events_ppl,data_scraped):
    '''
    Clean the data, merge the three files and returns a single datframe
    MVP: merging only the first two files
    '''
    # Clean data_events_ppl
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

    return data_merged

def get_data():
    # Get Local Data'
    # breakpoint()
    data_events_ppl = pd.read_csv(Path.join("raw_data", "240304 BPM Events list people  - ALL __.csv"))
    data_scraped = pd.read_csv(Path.join("raw_data", "result.csv"))
    # data_events_series = pd.read_csv(Path.join("..","raw_data", "BPM Events list people.csv"))

    return clean_data(data_events_ppl,data_scraped)

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
