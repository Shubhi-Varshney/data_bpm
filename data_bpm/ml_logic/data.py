import pandas as pd
import os.path as Path
from colorama import Fore, Style
from google.cloud import bigquery
import params

def clean_data():
    '''
    Clean the data, merge the three files and returns a single datframe
    '''
    return pd.DataFrame

def get_data():

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

        data_events_ppl = pd.read_csv(Path.join("..", "raw_data", "raw_all.csv"))
        data_scraped = pd.read_csv(Path.join("..","raw_data", "../raw_data/raw_scrapped.csv"))
        data_events_series = pd.read_csv(Path.join("..","raw_data", "raw_events.csv"))

    # Clean Data
    clean_data()
    return dict({'data_all' : data_events_ppl,
                 'data_dcrapped' : data_scraped,
                 'data_events' : data_events_series
    })

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
