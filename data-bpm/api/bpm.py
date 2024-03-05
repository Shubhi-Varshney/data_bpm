import pandas as pdf

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# app.state.model = load_model()

# @app.get('/predict')
# def suggestion(features):
#     # Compute attendee course suggestion 
#     model = app.state.model`
#     course = 1 # compute course selection -> to be done
    # model = app.state.model
    # assert model is not None

    # X_processed = preprocess_features(X_pred)
    # y_pred = model.predict(X_processed)

#     return {'course': y_pred}



@app.get("/")
def root():
    return {
        "greeting": "works!"
    }
