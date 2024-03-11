import pandas as pd
import numpy as np
import os.path as Path

from colorama import Fore, Style

from data_bpm.ml_logic.data import get_data, clean_data
from data_bpm.ml_logic.preprocessor import preprocess_features
from data_bpm.ml_logic.registry import load_model, save_model, save_results, load_preproc_pipeline
from data_bpm.ml_logic.model import train_model, train_model_2

def preprocess():
    data_for_ml, data_for_analytics = get_data()
    #print(data_for_analytics.sample(15))
    #print(data_for_analytics.info())
    # print(data_for_ml.sample(15))
    # print(data_for_ml.info())

    # ----- Toggle if you want to read the saved version of merged intermediate data
    # print(Fore.BLUE + "\n Reading the saved merged raw data.." + Style.RESET_ALL)
    # data_for_ml = pd.read_csv('../raw_data/data_for_ml.csv',index_col=0)
    # data_for_analytics = pd.read_csv('../raw_data/data_for_analytics.csv',index_col=0)
    # ----- Toggle if you want to read the saved version of merged intermediate data

    # ----- Toggle if you want to save a cleaned intermediate data
    print(Fore.BLUE + "\n Saving intermediate data to the raw_data.." + Style.RESET_ALL)
    data_for_ml.to_csv('raw_data/data_for_ml.csv')
    data_for_analytics.to_csv('raw_data/data_for_analytics.csv')
    # ------Toggle if you want to save a cleaned intermediate data

    X_processed = preprocess_features(data_for_ml.drop('Attendance', axis=1), save_pipeline = True)
    y_train = data_for_ml['Attendance']
    return (X_processed, y_train)

def train(save=False):
    """
    - Get the raw ML data
    - Preprocess it
    - Train the clustering model on the preprocessed dataset
    - Save the model and the labels
    """
    print(Fore.MAGENTA + "\n⭐️ Use case: train" + Style.RESET_ALL)

    print(Fore.BLUE + "\n Loading the pre-processing pipeline.." + Style.RESET_ALL)
    preproc_pipeline = load_preproc_pipeline()

    if preproc_pipeline == None:
        print("Failed to load preproc pipeline")
        print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
        X_processed, y_train = preprocess()
    else:
        # ----- Uncomment if want to train the model from already merged data ----- #
        # print(Fore.BLUE + "\n Reading the saved merged raw data.." + Style.RESET_ALL)
        # raw_ml_data = pd.read_csv("raw_data/data_for_ml.csv", index_col=0)
        # X_processed = preprocess_features(data_for_ml.drop('Attendance', axis=1))
        # y_train = data_for_ml['Attendance']
        # ----- Uncomment if want to train the model from already merged data ----- #

        raw_ml_data = get_data()[0]
        X_train = raw_ml_data.drop('Attendance', axis=1)
        X_processed = preproc_pipeline.transform(X_train)

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
    - Save the model
    """

    print(Fore.MAGENTA + "\n⭐️ Use case: train_model2" + Style.RESET_ALL)

    print(Fore.BLUE + "\n Loading the pre-processing pipeline.." + Style.RESET_ALL)
    preproc_pipeline = load_preproc_pipeline()

    if preproc_pipeline == None:
        print("Failed to load preproc pipeline")
        print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
        X_processed, y_train = preprocess()
    else:
        # ----- Uncomment if want to train the model from already merged data ----- #
        # print(Fore.BLUE + "\n Reading the saved merged raw data.." + Style.RESET_ALL)
        # raw_ml_data = pd.read_csv("raw_data/data_for_ml.csv", index_col=0)
        # X_processed = preprocess_features(data_for_ml.drop('Attendance', axis=1))
        # y_train = data_for_ml['Attendance']
        # ----- Uncomment if want to train the model from already merged data ----- #

        raw_ml_data = get_data()[0]
        X_train = raw_ml_data.drop('Attendance', axis=1)
        y_train = raw_ml_data['Attendance']
        X_processed = preproc_pipeline.transform(X_train)

    # Train model using `model.py`
    model = load_model()
    if model is None:
        print(Fore.BLUE + "\n Training the model.." + Style.RESET_ALL)

        # To train a classification model
        model = train_model_2(X_processed, y_train)

        # Save model
        if save == True:
            save_model(model)


def evaluate():
    pass

def pred():

    '''
    Predicting the probability of attending the event for a new/existing user
    '''
    breakpoint()
    X_pred = pd.read_csv("raw_data/predict.csv")
    preproc_pipeline = load_preproc_pipeline()

    if preproc_pipeline == None:
        print("Failed to load preproc pipeline")
        print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
        X_processed, y_train = preprocess()
        preproc_pipeline = load_preproc_pipeline()


    X_pred_process = preproc_pipeline.transform(X_pred)

    # Train model using `model.py`
    model = load_model()

    print(model.predict(X_pred_process))

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
    # train_model2(save=True)
    # evaluate()
    pred()
    # similar_users()
