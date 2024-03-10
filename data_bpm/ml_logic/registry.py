import glob
import os
import pickle
import time

from colorama import Fore, Style
from google.cloud import storage

from data_bpm.params import *

import mlflow
from mlflow.tracking import MlflowClient

import mlflow.sklearn

def save_model(model=None):
    """
    Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.pkl"
    - if MODEL_TARGET='mlflow', also persist it on MLflow
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save model locally
    model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", f"{timestamp}.pickle")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print("✅ Model saved locally")

    if MODEL_TARGET == "mlflow":
        mlflow.sklearn.log_model(
            sk_model=model,  # Sklearn model
            artifact_path="model",  # Artifact path within the run
            registered_model_name=MLFLOW_MODEL_NAME,  # Registered model name
            pickle_format="pickle"  # Use pickle format
        )

        print("✅ Model saved to MLflow")

    return None

def save_results(cleaned_ml_data, labels):
    '''
    Saving the cluster result to the original dataframe
    '''
    cleaned_ml_data['dbscan_cluster'] = labels
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", f"clusters_{timestamp}.csv")

    cleaned_ml_data.to_csv(model_path)


def load_model(stage="Production"):
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow'

    Return None (but do not Raise) if no model is found

    """

    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

        # Get the latest model version name by the timestamp on disk
        local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
        local_model_paths = glob.glob(f"{local_model_directory}/*")

        if not local_model_paths:
            return None

        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

        print(Fore.BLUE + f"\nLoading latest model from disk..." + Style.RESET_ALL)

        # Load model from disk using pickle
        with open(most_recent_model_path_on_disk, 'rb') as f:
            latest_model = pickle.load(f)

        print("✅ Model loaded from local disk")

        return latest_model

    elif MODEL_TARGET == "mlflow":
        print(Fore.BLUE + f"\nLoad [{stage}] model from MLflow..." + Style.RESET_ALL)

        # Load model from MLflow
        model = None
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        client = MlflowClient()

        try:
            model_versions = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[stage])
            model_uri = model_versions[0].source

            assert model_uri is not None
        except:
            print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {stage}")

            return None

        # Load model from MLflow artifact
        with mlflow.start_run():
            mlflow.sklearn.load_model(model_uri=model_uri)
            run_id = mlflow.active_run().info.run_id
            local_model_path = mlflow.get_artifact_uri().replace("file://", "")

        # Load the model from the local path
        with open(local_model_path, 'rb') as f:
            model = pickle.load(f)

        print("✅ Model loaded from MLflow")
        return model
    else:
        return None


def mlflow_transition_model(current_stage: str, new_stage: str) -> None:
    """
    Transition the latest model from the `current_stage` to the
    `new_stage` and archive the existing model in `new_stage`
    """
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient()

    version = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[current_stage])

    if not version:
        print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {current_stage}")
        return None

    client.transition_model_version_stage(
        name=MLFLOW_MODEL_NAME,
        version=version[0].version,
        stage=new_stage,
        archive_existing_versions=True
    )

    print(f"✅ Model {MLFLOW_MODEL_NAME} (version {version[0].version}) transitioned from {current_stage} to {new_stage}")

    return None


def mlflow_run(func):
    """
    Generic function to log params and results to MLflow along with TensorFlow auto-logging

    Args:
        - func (function): Function you want to run within the MLflow run
        - params (dict, optional): Params to add to the run in MLflow. Defaults to None.
        - context (str, optional): Param describing the context of the run. Defaults to "Train".
    """
    def wrapper(*args, **kwargs):
        mlflow.end_run()
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(experiment_name=MLFLOW_EXPERIMENT)

        with mlflow.start_run():
            mlflow.tensorflow.autolog()
            results = func(*args, **kwargs)

        print("✅ mlflow_run auto-log done")

        return results
    return wrapper

def save_preproc_pipeline(preproc_pipe=None):

    pipe_path = os.path.join(LOCAL_REGISTRY_PATH, "models","preproc_pipeline.pkl")
    print(Fore.BLUE + f"\nSaving preprocessing pipeline from local disk..." + Style.RESET_ALL)
    with open(pipe_path, 'wb') as f:
        pickle.dump(preproc_pipe, f)
        print("✅ Preprocessing pipeline saved locally")

    return None


def load_preproc_pipeline():
    # Load the fitted pipeline from the file

    local_pipe_path = os.path.join(LOCAL_REGISTRY_PATH, "models","preproc_pipeline.pkl")

    if not local_pipe_path:
        return None

    print(Fore.BLUE + f"\nLoad preprocessing pipeline from local disk..." + Style.RESET_ALL)

    with open('preproc_pipeline.pkl', 'rb') as f:
        preproc_pipe =  pickle.load(f)

    print("✅ Preprocessing pipeline loaded from local disk")
