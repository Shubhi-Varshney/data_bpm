from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVC
from scipy import stats

from colorama import Fore, Style
import pandas as pd
import numpy as np

from data_bpm import params

def train_model(
        X_processed : pd.DataFrame
    ) :

    """
    1. Get the pre-processed data from the pipeline
    2. Implement the model
    3. Return the model   """

    # $CODE_BEGIN
    print(Fore.BLUE + "\Training the model..." + Style.RESET_ALL)

    model = DBSCAN(eps=0.836842, min_samples=25)
    model.fit(X_processed)
    score = silhouette_score(X_processed, model.fit_predict(X_processed))
    no_of_clusters = len(np.unique(model.labels_))

    # $CODE_END

    print(f"✅ Model trained with clusters: {no_of_clusters} and silhouette_score: {score}")

    return model

def train_model_2(
        X_processed : pd.DataFrame,
        y_train : pd.DataFrame
    ) :

    """
    1. Get the pre-processed data from the pipeline
    2. Implement the classification model
    3. Return the model   """

    # $CODE_BEGIN
    print(Fore.BLUE + "\nTraining the model..." + Style.RESET_ALL)

    # Classification model to predict positive probability
    model = SVC(probability=True, class_weight='balanced')

    grid = {
            'C' : stats.uniform(0.1, 60),
            'kernel': ['linear', 'rbf', 'sigmoid'],
            'gamma' : stats.uniform(0.02, 0.06)
            }
    randsearch = RandomizedSearchCV(estimator=model, param_distributions=grid,
                                    n_iter=3000, scoring='precision',
                                    cv=3, n_jobs=-1, verbose=1)

    # Perform cross-validation with precision scoring
    randsearch.fit(X_processed, y_train)

    print(f"✅ SVM Model trained with best params: {randsearch.best_params_} and best score: {randsearch.best_score_}")

    return {
        "model" : randsearch.best_estimator_,
        "params" : randsearch.best_params_,
        "score" : randsearch.best_score_
        }


def get_similar_users(X_train_users_proc, X_new_user_proc):

    # return the indices of top_n similar users to the new user (used in prediction website)
    # X_train_users_proc = preprocessed final features of the training data
    # X_new_user_proc = preprocessed final features of the new user

    # Compute cosine similarity between the new user and each user in the training dataset
    similarities = cosine_similarity(X_new_user_proc.reshape(1, -1), X_train_users_proc)

    # Get indices of users sorted by cosine similarity (from highest to lowest)
    similar_users_indices = np.argsort(similarities)[0][::-1]

    # Select top-N similar users
    top_n = params.TOP_SIMILAR_USERS # Number of similar users to consider

    return similar_users_indices[:top_n]
