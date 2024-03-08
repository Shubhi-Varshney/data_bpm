from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score

from colorama import Fore, Style
import pandas as pd
import numpy as np


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
