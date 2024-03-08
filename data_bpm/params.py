import os
import numpy as np

MODEL_TARGET = 'local' # os.environ.get("MODEL_TARGET")

##################  GCP VARIABLES  ##################
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")

BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
INSTANCE = os.environ.get("INSTANCE")

# MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
# MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT")
# MLFLOW_MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME")
# Model Lifecycle
MLFLOW_TRACKING_URI='https://mlflow.lewagon.ai'
MLFLOW_EXPERIMENT='data_bpm_experiment_sydd'
MLFLOW_MODEL_NAME='data_bpm_experiment_sydd'

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(os.path.curdir(), "raw_data")
LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "data_bpm", "training_outputs")


##################  PREPROCESSOR PARAMS  #####################
COLUMN_NAMES_RAW = [ 'headline','description', 'jobTitle' ,'jobDescription','jobDuration', 'jobDateRange', 'jobTitle2', 'jobDuration2', 'schoolDateRange', 'skill1', 'skill2', 'skill3']
COLUMN_NAMES_METADATA = ['headline','description', 'jobTitle','jobDescription','jobTitle2', 'skill1', 'skill2', 'skill3']
SVD_COMPONENTS = 15
