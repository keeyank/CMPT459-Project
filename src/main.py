import pandas as pd
from pathlib import Path
from IPython.display import display
import matplotlib.pyplot as plt

# Helper Functions

def to_outcome_group(outcome):
    h = {'Discharged', 'Discharged from hospital', 'Hospitalized',
            'critical condition', 'discharge', 'discharged'}
    nh = {'Alive', 'Receiving Treatment', 'Stable', 'Under treatment',
            'recovering at home 03.03.2020', 'released from quarantine',
            'stable', 'stable condition'}
    d = {'Dead', 'Death', 'Deceased', 'Died', 'death', 'died'}
    r = {'Recovered', 'recovered'}

    if outcome in h: 
        return 'hospitalized'
    elif outcome in nh: 
        return 'nonhospitalized'
    elif outcome in d: 
        return 'deceased'
    elif outcome in r: 
        return 'recovered'

def clean_age_column(age):
    age = str(age)
    if not age.isdigit():
        x = age.split('-')
        y = age.split('.')
        #? '10-12', '0.75'
        if len(x) == 2:
            # '10-12'
            l, r = x
            # R could be '' empty in cases like 45-
            if r == '':
                d = int(l)
                return d
            d = (int(l) + int(r))//2
        if len(y) == 2:
            # '0.75'
            d = round(float(age))
        return d
    return int(age)

#1.1
cases_train = pd.read_csv('./data/cases_2021_train.csv')
cases_test = pd.read_csv('./data/cases_2021_test.csv')

outcomes = cases_train['outcome']
outcome_groups = outcomes.map(to_outcome_group)
cases_train['outcome_group'] = outcome_groups

#1.4

"""
Replace 80-89 with 85 using formula using the mean of extreme values
Round 12.9 with 13 the closest whole number
Remove Nan values
"""
cases_train.dropna(inplace=True, subset=['age'])
cases_test.dropna(inplace=True, subset=['age'])

# Remove records where age and sex and date attribute isn't provided using dropna
cases_train['age'] = cases_train.age.apply(clean_age_column)
cases_test['age'] = cases_test.age.apply(clean_age_column)

cases_train.dropna(subset=['sex'], inplace=True)
cases_test.dropna(subset=['sex'], inplace=True)

cases_train.dropna(subset=['date_confirmation'], inplace=True)
cases_test.dropna(subset=['date_confirmation'], inplace=True)

# Remove additional information attribute
cases_train.drop(columns=['additional_information'], inplace=True)
cases_test.drop(columns=['additional_information'], inplace=True)

# Export to csv
cases_train.to_csv('./data/cases_train_processed.csv')
cases_test.to_csv('./data/cases_test_processed.csv')

#display(cases_train)

#1.5
# Dealing with outliers
# Remove all the records with age more than 85
cases_train = cases_train[cases_train['age'] < 85]
cases_test = cases_test[cases_test['age'] < 85]

#1.6

# Update loc_train to match countries of cases_train
loc_train = pd.read_csv('./data/location_2021.csv')
loc_train['Country_Region'] = loc_train['Country_Region'].replace({'Korea, South': 'South Korea', 'US': 'United States'})

# Aggregate relevant statistics - group by Country
loc_train = loc_train.rename(columns={"Country_Region": "country"})
loc_train = loc_train.groupby('country').agg({'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum', 'Incident_Rate': 'mean', 'Case_Fatality_Ratio': 'mean'})
loc_train = loc_train.reset_index(level=0)

loc_train.to_csv('./data/location_2021_processed.csv')
#display(loc_train)

# Join the data frames for both training and test set
full_train = loc_train.merge(cases_train, 'inner', 'country')
full_test = loc_train.merge(cases_test, 'inner', 'country')

#1.7
# Remove redundant and irrelevant attributes
full_train.drop(columns=['Recovered'], inplace=True)
full_test.drop(columns=['Recovered'], inplace=True)
full_train.drop(columns=['province'], inplace=True)
full_test.drop(columns=['province'], inplace=True)
full_train.drop(columns=['source'], inplace=True)
full_test.drop(columns=['source'], inplace=True)
full_train.drop(columns=['outcome'], inplace=True)
full_test.drop(columns=['Confirmed'], inplace=True)
full_train.drop(columns=['Confirmed'], inplace=True)
full_test.drop(columns=['Deaths'], inplace=True)
full_train.drop(columns=['Deaths'], inplace=True)

full_train.to_csv('./data/cases_2021_train_processed.csv')
full_test.to_csv('./data/cases_2021_test_processed.csv')