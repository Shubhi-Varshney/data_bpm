import pandas as pd
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, StandardScaler
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

from data_bpm.ml_logic.data import load_data_to_bq
from data_bpm.ml_logic.encoders import transform_jobDateRange, transform_jobDuration, transform_SchoolPassed, transform_metadata
from data_bpm.params import *
def preprocess_features(X: pd.DataFrame):

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

    final_preprocessor = ColumnTransformer(
            [
                ("employment_pipe", employment_pipe, ["jobDateRange"]),
                ("job_duration_pipe", job_duration_pipe, ["jobDuration", "jobDuration2"] ),
                ("schoolPassed_pipe", schoolPassed_pipe, ["schoolDateRange"]),
                ('metadata_pipe', metadata_pipe, metadata_columns)
            ],
            remainder='passthrough',
        )

    X_processed = final_preprocessor.fit_transform(X)
    print(X_processed[:5, :5])

    print("✅ X_processed, with shape", X_processed.shape)

    return X_processed

    # After preprocessing, load the preprocessed data into bigquery
    # load_data_to_bq()
