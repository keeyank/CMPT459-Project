import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

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

cases_train = pd.read_csv('../data/cases_2021_train.csv')
outcomes = cases_train['outcome']

outcome_groups = outcomes.map(to_outcome_group)

cases_train['outcome_group'] = outcome_groups

cases_train.to_csv('../data/cases_2021_train_processed.csv')

#1.6
loc_train = pd.read_csv('../data/location_2021.csv')
loc_train['Country_Region'].replace({'Korea, South': 'South Korea', 'US': 'United States'})
loc_train.to_csv('../data/temp.csv')

#print(cases_train['outcome_group'])