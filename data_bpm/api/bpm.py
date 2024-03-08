
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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

# app.state.model = load_model()

@app.post("/predict")
def predict(payload: dict):
    """
    Make a single prediction for binary classification.
    """

    # Check if all required columns are present in the payload
    if not all(column in payload for column in COLUMN_NAMES_RAW):
        raise HTTPException(status_code=400, detail="Missing required columns in payload")

    # Convert payload to DataFrame
    X_pred = pd.DataFrame({column: [payload.get(column, '')] for column in COLUMN_NAMES_RAW})

    # Preprocess features if needed
    X_processed = preprocess_features(X_pred)

    # Make prediction
    try:
        # y_pred_proba = app.state.model.predict_proba(X_processed)
        # Assuming y_pred_proba is a single probability value for positive class
        positive_probability = 1 # float(y_pred_proba[0, 1])
        return {'probability_to_attend': positive_probability}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/")
def root():
    return {
        "greeting": "works!"
    }
