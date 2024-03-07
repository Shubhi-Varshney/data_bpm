import pandas as pd
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, StandardScaler
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

from data_bpm.ml_logic.data import load_data_to_bq
from data_bpm.ml_logic.encoders import transform_jobDateRange, transform_jobDuration, transform_SchoolPassed

def preprocess_features(X: pd.DataFrame):

    # Preprocess features
    # Feature Selection from the merged dataset
    selected_features = [ 'company', 'jobTitle', 'jobDuration', 'jobDateRange', 'jobTitle2', 'jobDuration2', 'schoolDateRange', 'schoolDegree', 'skill1', 'skill2', 'skill3']
    df = X[selected_features]

    # Function Transformer for employment
    employment_pipe = FunctionTransformer(transform_jobDateRange)

    # Function Transformer for jobDuration
    job_duration_pipe = FunctionTransformer(transform_jobDuration)

    # Function Transformer for SchoolDateRange
    schoolPassed_pipe = make_pipeline(
                        FunctionTransformer(transform_SchoolPassed),
                        SimpleImputer(strategy='mean')
    )


    final_preprocessor = ColumnTransformer(
            [
                ("employment_pipe", employment_pipe, ["jobDateRange"]),
                ("job_duration_pipe", job_duration_pipe, ["jobDuration", "jobDuration2"] ),
                ("schoolPassed_pipe", schoolPassed_pipe, ["schoolDateRange"] )
            ],
            remainder='passthrough',
        )

    X_processed = final_preprocessor.fit_transform(X)
    print(X_processed.head())

    print("✅ X_processed, with shape", X_processed.shape)

    return X_processed

    # After preprocessing, load the preprocessed data into bigquery
    # load_data_to_bq()
