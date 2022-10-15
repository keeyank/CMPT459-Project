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

