import pandas as pd
import numpy as np
import os.path as Path

from colorama import Fore, Style

from data_bpm.ml_logic.data import get_data, clean_data
from data_bpm.ml_logic.preprocessor import preprocess_features
from data_bpm.ml_logic.registry import load_model, save_model, save_results, load_preproc_pipeline
from data_bpm.ml_logic.model import train_model

def preprocess():
    # data_for_ml, data_for_analytics = get_data()
    #print(data_for_analytics.sample(15))
    #print(data_for_analytics.info())
    data_for_ml = pd.read_csv('raw_data/data_for_ml.csv',index_col=0)
    # data_for_analytics = pd.read_csv('raw_data/data_for_analytics.csv',index_col=0)
    print(data_for_ml.sample(15))
    print(data_for_ml.info())

    print(Fore.BLUE + "\n Saving intermediate data to the raw_data.." + Style.RESET_ALL)
    # Uncomment if you want to save a cleaned intermediate data
    # data_for_ml.to_csv('raw_data/data_for_ml.csv')
    # data_for_analytics.to_csv('raw_data/data_for_analytics.csv')

    X_processed = preprocess_features(data_for_ml.drop('Attendance', axis=1))
    y_train = data_for_ml['Attendance']
    return (X_processed,y_train)

def train(save=False):
    """
    - Get the raw ML data
    - Preprocess it
    - Train on the preprocessed dataset
    - Save the model and the labels
    """
    print(Fore.MAGENTA + "\n⭐️ Use case: train" + Style.RESET_ALL)

    print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
    X_processed, y_train = preprocess()

    raw_ml_data = pd.read_csv("raw_data/data_for_ml.csv")

    # Train model using `model.py`
    model = load_model()

    if model is None:
        print(Fore.BLUE + "\n Training the model.." + Style.RESET_ALL)
        model = train_model(X_processed)

        # To train a classification model
        # model = train_model(X_processed,y_train)
        # Save model
        save_model(model)

        # Save resuts
        # Saving the clusters returned by the model in the original raw ml_data
        save_results(raw_ml_data, model.labels_)

def train_model2(save=False):
    pass

def evaluate():
    pass

def pred():

    X_pred = pd.read_csv("raw_data/predict.csv")
    preproc_pipeline = load_preproc_pipeline()

    if preproc_pipeline == None:
        print("Failed to load preproc pipeline")

    X_processed = preproc_pipeline.transform(X_pred)
    # Train model using `model.py`
    model = load_model()
    print(model.predict(X_processed))

if __name__ == '__main__':
    preprocess()
    # train()
    # train_model2()
    # evaluate()
    pred()
