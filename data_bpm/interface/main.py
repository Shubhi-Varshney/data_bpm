import pandas as pd
import numpy as np
import os.path as Path
from data_bpm.ml_logic.data import get_data, clean_data
from data_bpm.ml_logic.preprocessor import preprocess_features

def preprocess():
    ## Load the data

    #return " @@@@ Hello "
    # data_for_ml, data_for_analytics = get_data()
    # print(data_for_ml)
    # print(data_for_ml.info())
    # print(data_for_analytics)
    # print(data_for_analytics.info())
    # data_for_analytics.to_csv('raw_data/data_for_analytics.csv')
    data_for_ml = pd.read_csv('raw_data/data_for_ml.csv')

    preprocess_features(data_for_ml)

def train():
    pass

def evaluate():
    pass

def pred():
    pass

if __name__ == '__main__':
    preprocess()
    # train()
    # evaluate()
    # pred()
