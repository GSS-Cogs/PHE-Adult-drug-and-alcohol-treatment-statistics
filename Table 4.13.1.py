# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Table 4.13.1: Mental health treatment need and treatment received 2017-18

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 4.13.1']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

cell = tab.filter('Mental health treatment need')
cell.assert_one()
observations = tab.filter('n').fill(DOWN).is_not_blank().is_not_whitespace()
Substance = cell.expand(DOWN).is_not_blank().is_not_whitespace()
Clients = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(Substance,'Treatment group',DIRECTLY,LEFT),
            HDim(Clients,'Clients in treatment',CLOSEST,LEFT),
            HDimConst('Measure Type','count-of-children'),
            HDimConst('Unit','clients-in-treatment'),
            HDimConst('Period', 'gregorian-interval/2017-04-01T00:00:00/P1Y')
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
if is_interactive():
    savepreviewhtml(c1)

new_table = c1.topandas()

import numpy as np
new_table['OBS'].replace('', np.nan, inplace=True)
new_table.dropna(subset=['OBS'], inplace=True)
new_table.rename(columns={'OBS': 'Value'}, inplace=True)
new_table['Value'] = new_table['Value'].astype(int)
new_table['Value'] = new_table['Value'].map(lambda x:''
                                  if (x == '-')
                                  else int(x))

new_table['Treatment group'].unique()

new_table['Basis of treatment'] = new_table['Treatment group'].map(
    lambda x: {
        'Mental health treatment need':'mental-health-treatment-need',
        'Community or other mental health services':'mental-health-treatment-need/community-or-other-mental-health-services',
        'Improving Access to Psychological Therapies (IAPT)':'mental-health-treatment-need/improving-access-to-psychological-therapies-iapt',
        'Primary care mental health treatment':'mental-health-treatment-need/primary-care-mental-health-treatment',
        'NICE recommended mental health treatment':'mental-health-treatment-need/nice-recommended-mental-health-treatment',
        'Identified space in a\xa0health based place of safety for\xa0mental health crises':'mental-health-treatment-need/identified-space-in-a-health-based-place-of-safety-for-mental-health-crises',
        'Total individuals receiving any treatment for mental health':'mental-health-treatment-need/total-individuals-receiving-any-treatment-for-mental-health',
        'No treatment received for a mental health treatment need':'mental-health-treatment-need/no-treatment-received-for-a-mental-health-treatment-need',
        'Missing':'mental-health-treatment-need/missing',
        'Total':'mental-health-treatment-need/total',
        'Total individuals needing mental health treatment':'mental-health-treatment-need/total-individuals-needing-mental-health-treatment',
        'Total number of new presentations':'mental-health-treatment-need/total-number-of-new-presentations',
        }.get(x, x))

import urllib.request as request
import csv
import io
import requests
vrl="https://raw.githubusercontent.com/ONS-OpenData/ref_alcohol/master/codelists/substance-type.csv"
t=requests.get(vrl).content
g=pd.read_csv(io.StringIO(t.decode('utf-8')))
new_table = pd.merge(new_table, g, how = 'left', left_on = 'Clients in treatment', right_on = 'Label')
new_table.columns = ['Substance type' if x=='Notation' else x for x in new_table.columns]
new_table = new_table[['Period','Basis of treatment','Substance type','Measure Type','Value','Unit']]

new_table


