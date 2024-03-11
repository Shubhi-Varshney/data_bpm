import pandas as pd
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.base import BaseEstimator, TransformerMixin
#from nltk.corpus import stopwords

from data_bpm.ml_logic.data import load_data_to_bq
from data_bpm.ml_logic.encoders import transform_jobDateRange, transform_jobDuration, transform_SchoolPassed, transform_metadata
from data_bpm.params import *
from data_bpm.ml_logic.registry import save_preproc_pipeline


class MetadataTransformer(TransformerMixin, BaseEstimator):
# TransformerMixin generates a fit_transform method from fit and transform
# BaseEstimator generates get_params and set_params methods

    def __init__(self, n_components):
        print("✅ MetadataTransformer constructor")
        self.count_vectorizer = None
        self.count_df = None
        self.n_components = n_components
        self.svd = TruncatedSVD(n_components=n_components)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if self.count_vectorizer == None:
            # transform is called for the first time
            print("✅ MetadataTransformer is called for the first time")
            # breakpoint()
            self.count_vectorizer = CountVectorizer(stop_words='english')
            self.count_vectorizer = self.count_vectorizer.fit(X.metadata)
            count_matrix = self.count_vectorizer.transform(X.metadata)
            self.count_df = pd.DataFrame(count_matrix.toarray(), index=X.index.tolist())
            self.svd = self.svd.fit(self.count_df)
            latent_df = self.svd.transform(self.count_df)
            return pd.DataFrame(latent_df)
        else:
            # called for prediction only
            print("✅ MetadataTransformer is called for PREDICT")
            count_vectorizer_pred = CountVectorizer(stop_words='english')
            count_matrix_pred = count_vectorizer_pred.fit_transform(X.metadata)
            count_matrix_pred_calc = pd.DataFrame(count_matrix_pred.toarray(), columns = count_vectorizer_pred.get_feature_names_out()).T
            count_matrix_calculate = pd.DataFrame(0,index = self.count_vectorizer.get_feature_names_out(), columns = [0])
            # match the vocabulary
            for index in count_matrix_pred_calc.index:
                if index in count_matrix_calculate.index:
                    count_matrix_calculate.loc[index, 0] = count_matrix_pred_calc.loc[index, 0]
            latent_df = self.svd.transform(count_matrix_calculate.reset_index(drop=True).T)
            return pd.DataFrame(latent_df)
    # count = CountVectorizer(stop_words='english')
    # count_matrix = count.fit_transform(df['metadata'])
    # count_df = pd.DataFrame(count_matrix.toarray(), index=df.index.tolist())

    # # Apply SVD
    # svd = TruncatedSVD(n_components=params.SVD_COMPONENTS)
    # latent_df = svd.fit_transform(count_df)


    # return pd.DataFrame(latent_df)

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

    metadata_pipe = Pipeline([
            ('transform_metadata', FunctionTransformer(transform_metadata)),
            ('custom_transformer', MetadataTransformer(n_components = SVD_COMPONENTS))
        ])
    preprocessor_pipe = ColumnTransformer(
            [
                ("employment_pipe", employment_pipe, ["jobDateRange"]),
                ("job_duration_pipe", job_duration_pipe, ["jobDuration", "jobDuration2"] ),
                ("schoolPassed_pipe", schoolPassed_pipe, ["schoolDateRange"]),
                ('metadata_pipe', metadata_pipe, metadata_columns)
            ],
            remainder='drop',
        )

    final_preprocessor = Pipeline([
                                ('preprocessor', preprocessor_pipe),
                                ('scaler', MinMaxScaler())
                                ])

    final_preprocessor = final_preprocessor.fit(X)
    X_processed = final_preprocessor.transform(X)
    # print(X_processed[:5, :5])

    print("✅ X_processed, with shape", X_processed.shape)

    print(X_processed)

    if save_pipeline == True:
        save_preproc_pipeline(final_preprocessor)

    return X_processed

    # After preprocessing, load the preprocessed data into bigquery
    # load_data_to_bq()
