import pandas as pd
import datetime
import numpy as np

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
         4 months = 5 mon (parts = 2)
    '''
    parts = X.applymap(lambda x: str(x).split())
    years = 0
    months = 0

    # Getting the exact element of years and months
    if len(parts) == 4:
        years = int(parts[0])
        months = int(parts[2])
    elif len(parts) == 2:
        years = 0
        months = int(parts[0])

    total_mos = (years * 12) + months
    return total_mos


def transform_SchoolPassed(X):
    '''
    Extracts the last year of school Date range and calculate the no.
    of years from current year since he passed his last school
    '''
    def calc_years(schoolyear):
        breakpoint()
        if ~pd.isna(schoolyear):
            tokens = str(schoolyear).split()
            year_schoolEnd = int(tokens[-1])

            # Get the current date
            current_date = datetime.datetime.now()

            # Extract the year from the current date
            current_year = current_date.year
            years = int(current_year - year_schoolEnd)
        else :
            years = np.nan
        return years

    years = X.apply(lambda x : calc_years(x), axis = 1)
    return years

def transform_location(X: pd.DataFrame):
    ''''
    Locations are given as City, city, COuntry etc.
    We are extracting first word and dropping other values other than Berlin as we are targetting for people who are based in Berlin
    '''

    assert isinstance(X, pd.DataFrame)

    X['location'] = X['location'].str.split(',').str[0]
    return X[X['location'] == 'Berlin']
