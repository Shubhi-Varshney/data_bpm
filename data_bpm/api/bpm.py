
import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import json
from data_bpm.ml_logic.registry import load_model, load_preproc_pipeline
from data_bpm.ml_logic.data import get_data_from_gcs, save_data_to_gcs
from data_bpm.interface.main import *
from data_bpm.params import *
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.state.model = load_model()
app.state.preproc_pipe = load_preproc_pipeline()

@app.post("/predict")
def predict(File: UploadFile=File(...)):
    content = File.file.read()
    decode = content.decode('utf-8')
    df_json = json.loads(decode)
    X_pred = pd.DataFrame(df_json)
    print(X_pred)
    X_processed = app.state.preproc_pipe.transform(X_pred)
    print(X_processed)
    # Make prediction
    try:
        y_pred_proba = app.state.model.predict_proba(X_processed)
        # Assuming y_pred_proba is a single probability value for positive class
        positive_probability = float(y_pred_proba[0, 1])
        return {'probability_to_attend': positive_probability}
        # return app.state.model.predict(X_processed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# def predict(payload: dict):
#     """
#     Make a single prediction for binary classification.
#     """

#     # Check if all required columns are present in the payload
#     if not all(column in payload for column in COLUMN_NAMES_RAW):
#         raise HTTPException(status_code=400, detail="Missing required columns in payload")

#     # Convert payload to DataFrame
#     X_pred = pd.DataFrame({column: [payload.get(column, '')] for column in COLUMN_NAMES_RAW})

#     # Preprocess features if needed
#     X_processed = preprocess_features(X_pred)

#     # Make prediction
#     try:
#         # y_pred_proba = app.state.model.predict_proba(X_processed)
#         # Assuming y_pred_proba is a single probability value for positive class
#         positive_probability = 1 # float(y_pred_proba[0, 1])
#         return {'probability_to_attend': positive_probability}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



@app.get("/")
def root():
    return {
        "greeting": "works!"
    }

@app.get("/getCleanData")
def getCleanData():
    # 1. Load the latest data files from google cloud storage
    # 2. Merge and clean the data
    # 3. Save the cleaned data on google cloud storage again for dashboard
    # 4. If everythin OK, return a OK message otherwise an appropriate error message

    ## Doing 1st and 2nd steps
    success, result = get_data_from_gcs()

    if success:
        data_ml, data_analytics = result[0], result[1]

        ## Doing 3rd and 4th steps
        save_flag, message = save_data_to_gcs(data_ml, data_analytics)
        if save_flag :
            return {
                "Success" : "Cleaned Files saved in GCS, {message}"
            }
        else :
            return {
                "Error" : f"Unable to save the cleaned data in GCS, {message}"
            }
    else :
        return {
            "Error" : f"Unable to load file from GCS, {result}"
        }


# @app.get("/train")
# def train():
#     # 1. read the latest clean data from google cloud
#     # 2. preprocess it
#     # 3. train the model


#     return {
#         "greeting": "works!"
#     }
