import pandas as pd
import numpy as np
import os.path as Path
from data_bpm.ml_logic.data import get_data, clean_data

def preprocess():
    #breakpoint()
    ## Load the data
    data_for_ml, data_for_analytics = get_data()
    print(data_for_ml)
    print(data_for_ml.info())
    print(data_for_analytics)
    print(data_for_analytics.info())
    # clean_data()

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
