import pandas as pd
import datetime
import numpy as np
import re # REGEX
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def transform_jobDateRange(X: pd.DataFrame):
    '''
    Transform Current JobDateRange into working status:
    If JobDateRange is like Oct 2022 to present --> Employed
    If JobDateRange is like Oct 2022 to Dec 2023 --> Unemployed
    '''

    assert isinstance(X, pd.DataFrame)

    working = X['jobDateRange'].astype(str).apply(lambda x : 1 if x.endswith('Present') else 0)

    emp_dic = dict(
                employment_status = working
            )

    return pd.DataFrame(emp_dic)

def transform_jobDuration(X: pd.DataFrame):
    '''
    Transforming Job Duration from linked in months.
    e.g. 2 years 10 months = 34 mon (parts = 4)
         4 months = 4 mon (parts = 2)
    '''

    def calc_months(duration):
        parts = str(duration).split()
        years = 0
        months = 0

        # Getting the exact element of years and months
        if len(parts) == 4:
            years = int(parts[0])
            months = int(parts[2])
        elif len(parts) == 2:
            if parts[1] == 'yr':
                years = int(parts[0])
                months = 0
            elif parts[1] == 'mos':
                years = 0
                months = int(parts[0])

        total_mos = (years * 12) + months
        return total_mos

    X['jobDuration'] = X['jobDuration'].apply(lambda x: calc_months(x))

    X['jobDuration2'] = X['jobDuration2'].apply(lambda x: calc_months(x))

    return X[['jobDuration', 'jobDuration2']]



def transform_SchoolPassed(X):
    '''
    Extracts the last year of school Date range and calculate the no.
    of years from current year since he passed his last school
    '''
    def calc_years(schoolyear):
        if pd.isna(schoolyear):
           years = np.nan
        else :
            tokens = str(schoolyear).split()
            year_schoolEnd = int(tokens[-1])

            # Get the current date
            current_date = datetime.datetime.now()

            # Extract the year from the current date
            current_year = current_date.year
            years = int(current_year - year_schoolEnd)
        return years

    years = X.map(lambda x : calc_years(x))
    return years

def transform_location(X: pd.DataFrame):
    ''''
    Locations are given as City, city, COuntry etc.
    We are extracting first word and dropping other values other than Berlin as we are targetting for people who are based in Berlin
    '''

    assert isinstance(X, pd.DataFrame)

    X['location'] = X['location'].str.split(',').str[0]
    return X[X['location'] == 'Berlin']

def transform_metadata(df):
    df.fillna("", inplace=True)

    df['metadata'] = df.apply(lambda row: ' '.join(row), axis=1)

    df['metadata'] = df.metadata.apply(basic_cleaning)
    df['metadata'] = df.metadata.apply(remove_stopwords)
    df['metadata'] = df.metadata.apply(lemma)

    return df[['metadata']]

    # count = CountVectorizer(stop_words='english')
    # count_matrix = count.fit_transform(df['metadata'])
    # count_df = pd.DataFrame(count_matrix.toarray(), index=df.index.tolist())

    # # Apply SVD
    # svd = TruncatedSVD(n_components=params.SVD_COMPONENTS)
    # latent_df = svd.fit_transform(count_df)


    # return pd.DataFrame(latent_df)


def basic_cleaning(sentence):

    # 1. Removing whitespaces
    sentence = sentence.strip()

    # 2. Lowercasing
    sentence = sentence.lower()

    # 3. Removing numbers
    sentence = ''.join(char for char in sentence if not char.isdigit())

    # remove tags
    sentence = re.sub('<[^<]+>', "", sentence)

    # 4. Removing punctuation
    for punctuation in string.punctuation:
        sentence = sentence.replace(punctuation, '')

    #5 remove non-alpha characters
    sentence = sentence.replace(r'[^a-zA-Z\s]', '')

    return sentence

stop_words = set(stopwords.words('english'))

def remove_stopwords (text):
    tokenized = word_tokenize(text)
    without_stopwords = [word for word in tokenized if not word in stop_words]
    return without_stopwords


def lemma(text):
    lemmatizer = WordNetLemmatizer() # Instantiate lemmatizer
    lemmatized = [lemmatizer.lemmatize(word) for word in text] # Lemmatize
    lemmatized_string = " ".join(lemmatized)
    return lemmatized_string
