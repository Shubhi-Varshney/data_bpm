
import pandas as pd
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import json
from data_bpm.ml_logic.registry import load_model, load_preproc_pipeline
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
