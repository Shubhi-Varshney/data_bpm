import pandas as pd
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, MinMaxScaler
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

from data_bpm.ml_logic.data import load_data_to_bq
from data_bpm.ml_logic.encoders import transform_jobDateRange, transform_jobDuration, transform_SchoolPassed, transform_metadata
from data_bpm.params import *
from data_bpm.ml_logic.registry import save_preproc_pipeline

def preprocess_features(X: pd.DataFrame, save_pipeline = True):

    # Preprocess features
    # Feature Selection from the merged dataset


    selected_features = COLUMN_NAMES_RAW
    metadata_columns = COLUMN_NAMES_METADATA
    X = X[selected_features]

    # Function Transformer for employment
    employment_pipe = FunctionTransformer(transform_jobDateRange)

    # Function Transformer for jobDuration
    job_duration_pipe = FunctionTransformer(transform_jobDuration)

    # Function Transformer for SchoolDateRange
    schoolPassed_pipe = make_pipeline(
                        FunctionTransformer(transform_SchoolPassed),
                        SimpleImputer(strategy='mean')
    )

    metadata_pipe = FunctionTransformer(transform_metadata)

    preprocessor_pipe = ColumnTransformer(
            [
                ("employment_pipe", employment_pipe, ["jobDateRange"]),
                ("job_duration_pipe", job_duration_pipe, ["jobDuration", "jobDuration2"] ),
                ("schoolPassed_pipe", schoolPassed_pipe, ["schoolDateRange"]),
                ('metadata_pipe', metadata_pipe, metadata_columns)
            ],
            remainder='passthrough',
        )

    final_preprocessor = make_pipeline(
                preprocessor_pipe,
                MinMaxScaler()
    )

    final_preprocessor = final_preprocessor.fit(X)
    X_processed = final_preprocessor.transform(X)
    # print(X_processed[:5, :5])

    print("✅ X_processed, with shape", X_processed.shape)

    if save_pipeline == True:
        save_preproc_pipeline(final_preprocessor)

    return X_processed
