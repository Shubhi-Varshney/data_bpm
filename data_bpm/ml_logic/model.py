from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity

from colorama import Fore, Style
import pandas as pd
import numpy as np

from data_bpm import params

def train_model(
        X_processed : pd.DataFrame
    ) :

    """
    1. Get the raw data
    2. Get the pre-processed data from the pipeline
    3. Implement the model
    4. Return the model   """

    # $CODE_BEGIN
    print(Fore.BLUE + "\nPreprocessing the model..." + Style.RESET_ALL)

    model = DBSCAN(eps=0.836842, min_samples=25)
    model.fit(X_processed)
    score = silhouette_score(X_processed, model.fit_predict(X_processed))
    no_of_clusters = len(np.unique(model.labels_))

    # $CODE_END

    print(f"✅ Model trained with clusters: {no_of_clusters} and silhouette_score: {score}")

    return model


def similar_users(X_train_users_proc, X_new_user_proc):

    # return the indices of top_n similar users to the new user (used in prediction website)
    # X_train_users_proc = preprocessed final features of the trianing data
    # X_new_user_proc = preprocessed final features of the new user

    # Compute cosine similarity between the new user and each user in the training dataset
    similarities = cosine_similarity(X_new_user_proc.reshape(1, -1), X_train_users_proc)

    # Get indices of users sorted by cosine similarity (from highest to lowest)
    similar_users_indices = np.argsort(similarities)[0][::-1]

    # Select top-N similar users
    top_n = params.TOP_SIMILAR_USERS # Number of similar users to consider

    return similar_users_indices[:top_n]
