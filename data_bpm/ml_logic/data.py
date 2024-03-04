import pandas as pd
import os.path as Path

def clean_data():
    '''
    Clean the data, merge the three files and returns a single datframe
    '''
    return pd.DataFrame

def get_data():
    # Get Local Data
    data_events_ppl = pd.read_csv(Path.join("..", "raw_data", "240304 BPM Events list people  - ALL __.csv"))
    data_scraped = pd.read_csv(Path.join("..","raw_data", "../raw_data/result.csv"))
    data_events_series = pd.read_csv(Path.join("..","raw_data", "BPM Events list people"))

    clean_data()

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
