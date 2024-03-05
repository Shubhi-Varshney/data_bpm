import pandas as pd
from data_bpm.ml_logic.data import load_data_to_bq

def preprocess_features(X: pd.DataFrame):

    # To Do:
    # Preprocess features
    # After preprocessing, load the preprocessed data into bigquery
    load_data_to_bq()
