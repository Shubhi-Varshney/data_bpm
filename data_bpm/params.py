import os
import numpy as np

MODEL_TARGET = os.environ.get("MODEL_TARGET")
DATA_TARGET = os.environ.get("DATA_TARGET")

##################  GCP VARIABLES  ##################
GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")

BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_REGION = os.environ.get("BQ_REGION")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
RAW_FILE_EVENT = os.environ.get("RAW_FILE_EVENT")
RAW_FILE_SCRAPPED = os.environ.get("RAW_FILE_SCRAPPED")
CLEANED_FILE_ML = os.environ.get("CLEANED_FILE_ML")
CLEANED_FILE_ANALYTICS = os.environ.get("CLEANED_FILE_ANALYTICS")
INSTANCE = os.environ.get("INSTANCE")

# MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
# MLFLOW_EXPERIMENT = os.environ.get("MLFLOW_EXPERIMENT")
# MLFLOW_MODEL_NAME = os.environ.get("MLFLOW_MODEL_NAME")
# Model Lifecycle
MLFLOW_TRACKING_URI='https://mlflow.lewagon.ai'
MLFLOW_EXPERIMENT='data_bpm_experiment_sydd'
MLFLOW_MODEL_NAME='data_bpm_experiment_sydd'

##################  CONSTANTS  #####################

# LOCAL_DATA_PATH = os.path.join(os.path.curdir(), "raw_data")
# LOCAL_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), ".lewagon", "data_bpm", "training_outputs")
# LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "data_bpm", "training_outputs")
# LOCAL_REGISTRY_PATH = os.path.join(PROJECT_ROOT, ".lewagon", "data_bpm", "training_outputs")

# LOCAL_REGISTRY_PATH =  '~/.lewagon/data_bpm'
# LOCAL_REGISTRY_PATH =  '/home/shubhi/.lewagon/data_bpm'
# LOCAL_DATA_PATH = os.path.join(os.path.curdir(), "raw_data")

# IS_DOCKER = os.environ.get('DOCKER_ENV', False)

##################  CONSTANTS  #####################
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOCAL_REGISTRY_PATH = os.path.join(PROJECT_ROOT, "training_outputs")

##################  PREPROCESSOR PARAMS  #####################
COLUMN_NAMES_RAW = [ 'headline','description', 'jobTitle' ,'jobDescription','jobDuration', 'jobDateRange', 'jobTitle2', 'jobDuration2', 'schoolDateRange', 'skill1', 'skill2', 'skill3']
COLUMN_NAMES_METADATA = ['headline','description', 'jobTitle','jobDescription','jobTitle2', 'skill1', 'skill2', 'skill3']
SVD_COMPONENTS = 18
TOP_SIMILAR_USERS = 10
