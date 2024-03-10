import pandas as pd
import numpy as np
import os.path as Path

from colorama import Fore, Style

from data_bpm.ml_logic.data import get_data, clean_data
from data_bpm.ml_logic.preprocessor import preprocess_features
from data_bpm.ml_logic.registry import load_model, save_model, save_results
from data_bpm.ml_logic.model import train_model

def preprocess():
    data_for_ml, data_for_analytics = get_data()
    print(data_for_analytics.sample(15))
    print(data_for_analytics.info())
    # print(data_for_analytics)
    # print(data_for_analytics.info())
    # data_for_ml = pd.read_csv('../raw_data/data_for_ml.csv',index_col=0)
    # data_for_analytics = pd.read_csv('../raw_data/data_for_analytics.csv',index_col=0)

    # Uncomment if you want to save a cleaned intermediate data
    data_for_ml.to_csv('raw_data/data_for_ml.csv')
    data_for_analytics.to_csv('raw_data/data_for_analytics.csv')

def train(save=False):
    """
    - Get the raw ML data
    - Preprocess it
    - Train the clustering model on the preprocessed dataset
    - Save the model and the labels
    """
    print(Fore.MAGENTA + "\n⭐️ Use case: train" + Style.RESET_ALL)

    raw_ml_data = pd.read_csv("raw_data/data_for_ml.csv")
    print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
    X_processed = preprocess_features(raw_ml_data)

    # Train model using `model.py`
    model = load_model()

    if model is None:
        print(Fore.BLUE + "\n Training the model.." + Style.RESET_ALL)
        model = train_model(X_processed)

        # Save model
        if save == True:
            save_model(model)
            # Save resuts
            # Saving the clusters returned by the model in the original raw ml_data
            save_results(raw_ml_data, model.labels_)


def train_model2(save=False):
    """
    - Get the raw ML data
    - Preprocess it
    - Train the classification model on the preprocessed dataset
    - Save the model and the labels
    """
    print(Fore.MAGENTA + "\n⭐️ Use case: train_model2" + Style.RESET_ALL)

    raw_ml_data = pd.read_csv("raw_data/data_for_ml.csv")
    print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
    X_processed = preprocess_features(raw_ml_data)

    # Train model using `model.py`
    model = load_model()

    if model is None:
        print(Fore.BLUE + "\n Training the model.." + Style.RESET_ALL)
        model = train_model(X_processed)

        # Save model
        if save == True:
            save_model(model)
            # Save resuts
            # Saving the clusters returned by the model in the original raw ml_data
            save_results(raw_ml_data, model.labels_)

def evaluate():
    pass

def pred():

    X_pred = pd.read_csv("raw_data/predict.csv")
    X_processed = preprocess_features(X_pred)

    # Train model using `model.py`
    model = load_model()
    print(model.predict(X_processed))

def similar_users():
    '''
    Find top n similar users of a new/existing user
    '''
    raw_ml_data = pd.read_csv("raw_data/data_for_ml.csv")
    print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)

    # preprocess_pipeline = load_preprocessor()

    print(Fore.BLUE + "\n Reading the predict.csv.." + Style.RESET_ALL)
    X_pred = pd.read_csv("raw_data/predict.csv")

    # X_processed = preprocess_features(raw_ml_data)
    # X_processed_train = preprocess_pipeline.transform(raw_ml_data)
    # X_processed_pred = preprocess_pipeline.transform(X_pred)



if __name__ == '__main__':
    # preprocess()
    # train()
    train_model2()
    # evaluate()
    # pred()
    similar_users()
