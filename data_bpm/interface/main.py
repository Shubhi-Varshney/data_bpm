import pandas as pd
import numpy as np
import os.path as Path
from data-bpm.ml-logic.data import get_data, clean_data

def preprocess():

    ## Load the data
    get_data()
    clean_data()

def train():
    pass

def evaluate():
    pass

def pred():
    pass

if __name__ == '__main__':
    preprocess()
    train()
    evaluate()
    pred()
