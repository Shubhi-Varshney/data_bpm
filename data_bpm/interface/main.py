import pandas as pd
import numpy as np
import os.path as Path

from colorama import Fore, Style

from data_bpm.ml_logic.data import get_data, clean_data, save_data_to_gcs
from data_bpm.ml_logic.preprocessor import preprocess_features
from data_bpm.ml_logic.registry import load_model, save_model, save_results, load_preproc_pipeline
from data_bpm.ml_logic.model import train_model, train_model_2
from data_bpm import params
from data_bpm.ml_logic.model import get_similar_users

def preprocess():
    data_for_ml, data_for_analytics = get_data()
    #print(data_for_analytics.sample(15))
    #print(data_for_analytics.info())
    # print(data_for_ml.sample(15))
    # print(data_for_ml.info())

    # ----- Toggle if you want to read the saved version of merged intermediate data
    # print(Fore.BLUE + "\n Reading the saved merged raw data.." + Style.RESET_ALL)
    # data_for_ml = pd.read_csv('raw_data/data_for_ml.csv',index_col=0)
    # data_for_analytics = pd.read_csv('raw_data/data_for_analytics.csv',index_col=0)

    # ----- Toggle if you want to save a cleaned intermediate data
    if params.DATA_TARGET == 'local':
        print(Fore.BLUE + "\n Saving intermediate clean data to the raw_data folder.." + Style.RESET_ALL)
        data_for_ml.to_csv(f'raw_data/{params.CLEANED_FILE_ML}')
        data_for_analytics.to_csv(f'raw_data/{params.CLEANED_FILE_ANALYTICS}')
    elif params.DATA_TARGET == 'gcs':
        print(Fore.BLUE + "\n Saving intermediate clean data to the gcs.." + Style.RESET_ALL)
        save_data_to_gcs(data_for_ml, data_for_analytics)

    # X_processed = preprocess_features(data_for_ml.drop(columns=['Attendance']), save_pipeline = True)
    # y_train = data_for_ml['Attendance']
    # return (X_processed, y_train)

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

        raw_ml_data = get_data()[0]
        X_train = raw_ml_data.drop(columns=['Attendance'])
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

    try :

        print(Fore.MAGENTA + "\n⭐️ Use case: train_model2" + Style.RESET_ALL)

        if params.DATA_TARGET == 'local':

            print(Fore.BLUE + "\n Reading the clean data from local folder: raw_data.." + Style.RESET_ALL)
            data_for_ml = pd.read_csv(f"raw_data/{params.CLEANED_FILE_ML}", index_col=0)

        elif params.DATA_TARGET == 'gcs':

            print(Fore.BLUE + "\n Reading the clean data from gcs .." + Style.RESET_ALL)
            bucket_name = params.BUCKET_NAME
            gsfile_path_events_ppl = f'gs://{bucket_name}/{params.CLEANED_FILE_ML}'
            data_for_ml = pd.read_csv(gsfile_path_events_ppl)


        X_processed = preprocess_features(data_for_ml.drop(columns=['Attendance']), save_pipeline = True)
        y_train = data_for_ml['Attendance']

        # print(Fore.BLUE + "\n Loading the pre-processing pipeline.." + Style.RESET_ALL)
        # preproc_pipeline = load_preproc_pipeline()

        # if preproc_pipeline == None:
        #     print("Failed to load preproc pipeline")
        #     print(Fore.BLUE + "\n Preprocessing the raw data.." + Style.RESET_ALL)
        #     X_processed, y_train = preprocess()
        # else:
        #     # ----- Uncomment if want to train the model from already merged data ----- #
        #     print(Fore.BLUE + "\n Reading the saved merged raw data.." + Style.RESET_ALL)
        #     data_for_ml = pd.read_csv("raw_data/data_for_ml.csv", index_col=0)
        #     # X_processed = preprocess_features(data_for_ml.drop('Attendance', axis=1))
        #     # y_train = data_for_ml['Attendance']
        #     #
        #     y_train = data_for_ml['Attendance']
        #     X_processed = preproc_pipeline.transform(data_for_ml.drop(columns=['Attendance']))

        # # Train model using `model.py`
        # model = load_model()
        # if model is None:

        # To train a classification model
        model_dic = train_model_2(X_processed, y_train)
        model = model_dic['model']

        # Save model
        if save == True:
            save_model(model)

    except Exception as e:
        return False, e

    return (True, model_dic)

def evaluate():
    pass

def pred():

    '''
    Predicting the probability of attending the event for a new/existing user
    '''
    X_pred = pd.read_csv("raw_data/predict.csv")
    preproc_pipeline = load_preproc_pipeline()

    # Commented | As we commented preprocess_features in preprocess method
    # if preproc_pipeline == None:
    #     print(Fore.BLUE + "\n Failed to load preproc pipeline \n Preprocessing the raw data.." + Style.RESET_ALL)
    #     X_processed, y_train = preprocess()
    #     preproc_pipeline = load_preproc_pipeline()

    X_pred_process = preproc_pipeline.transform(X_pred)

    # Train model using `model.py`
    model = load_model()

    # Predict probability of a person to attend
    probabilities = model.predict_proba(X_pred_process)

    # Get probability of positive result (class 1)
    positive_probabilities = probabilities[:, 1]

    print(positive_probabilities)

def similar_users():
    '''
    Find top n similar users of a new/existing user   '''

    if params.DATA_TARGET == 'local':

        print(Fore.BLUE + "\n Reading the clean data from local folder: raw_data.." + Style.RESET_ALL)
        data_for_ml = pd.read_csv(f"raw_data/{params.CLEANED_FILE_ML}", index_col=0)

    elif params.DATA_TARGET == 'gcs':

        print(Fore.BLUE + "\n Reading the clean data from gcs .." + Style.RESET_ALL)
        bucket_name = params.BUCKET_NAME
        gsfile_path_events_ppl = f'gs://{bucket_name}/{params.CLEANED_FILE_ML}'
        data_for_ml = pd.read_csv(gsfile_path_events_ppl)

    print(Fore.BLUE + "\n Reading the predict.csv.." + Style.RESET_ALL)
    X_pred = pd.read_csv("raw_data/predict.csv")

    preproc_pipeline = load_preproc_pipeline()

    # Commented | As we commented preprocess_features in preprocess method
    # if preproc_pipeline == None:
    #     print(Fore.BLUE + "\n Failed to load preproc pipeline \n Preprocessing the raw data.." + Style.RESET_ALL)
    #     X_processed, y_train = preprocess()
    #     preproc_pipeline = load_preproc_pipeline()

    X_train_process = preproc_pipeline.fit_transform(data_for_ml)
    X_pred_process = preproc_pipeline.transform(X_pred)

    user_id_indices = get_similar_users(X_train_process, X_pred_process)
    #print(data_for_ml.iloc[user_id_indices][['fullName', 'company', 'jobTitle']])

    users_info = data_for_ml.iloc[user_id_indices][['fullName', 'company', 'jobTitle']]
    users_info.index = users_info.index.astype(int)

    user_dict = users_info.to_dict(orient='index')

    print(user_dict)

if __name__ == '__main__':
    # preprocess()
    # train()
    # train_model2(save=True)
    # evaluate()
    # pred()
    similar_users()
