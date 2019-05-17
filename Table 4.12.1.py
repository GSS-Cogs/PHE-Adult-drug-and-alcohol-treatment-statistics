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

# Table 4.12.1: Parental status of new presentations to treatment 2017-18	

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

new_table = pd.DataFrame()

tab = tabs['Table 4.12.1']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

# +
cell = tab.filter('Parental status')
Parentalstatus = cell.expand(DOWN).is_not_blank().is_not_whitespace()
Clients = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
obs =  tab.filter('F').shift(1,0).fill(DOWN) | tab.filter('M').shift(1,0).fill(DOWN) |\
         tab.filter('F').fill(DOWN) | tab.filter('M').fill(DOWN) 
ts = tab.filter('Incomplete data').shift(0,1).expand(RIGHT)
observations = Clients.fill(DOWN).is_not_blank().is_not_whitespace() - Parentalstatus
observations = observations.is_number() - obs -ts
Dimensions = [
            HDim(Parentalstatus,'Treatment group',DIRECTLY,LEFT),
            HDim(Clients,'Clients in treatment',DIRECTLY,ABOVE),
            HDimConst('Measure Type','count-of-new-presentations-to-treatment'),
            HDimConst('Unit','new-presentations-to-treatment'),
            HDimConst('Period', 'gregorian-interval/2017-04-01T00:00:00/P1Y')
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
if is_interactive():
        savepreviewhtml(c1)
# -

table = c1.topandas()

import numpy as np
table['OBS'].replace('', np.nan, inplace=True)
table.dropna(subset=['OBS'], inplace=True)
table.rename(columns={'OBS': 'Value'}, inplace=True)
table['Value'] = table['Value'].astype(int)
table['Value'] = table['Value'].map(lambda x:''
                                  if (x == '-')
                                  else int(x))

table['treatment'] = table['Treatment group'] + ' - Total'

table['Basis of treatment'] = table['treatment'].map(
    lambda x: {
        'Parental status':'parental-status',
        'Parent living with children - Total':'parental-status/parent-living-with-children-total',
        'Other contact living with children - Total':'parental-status/other-contact-living-with-children-total',
        'Parents not with children - Total':'parental-status/parents-not-with-children-total',
        'Not parent no contact with children - Total':'parental-status/not-parent-no-contact-with-children-total',
        'Incomplete data - Total':'parental-status/incomplete-data-total',
        'Total - Total':'parental-status/total-total'
        }.get(x, x))

table = table[['Period','Basis of treatment','Clients in treatment','Measure Type','Value','Unit']]

table.head()

new_table = pd.concat([new_table, table])

tab = tabs['Table 4.12.1']

# +
cell = tab.filter('Parental status')
Sex = tab.filter('F') | tab.filter('M')
Clients = Sex.shift(0,-1).expand(RIGHT).is_not_blank().is_not_whitespace()
ts = tab.filter('Incomplete data').shift(0,1).expand(RIGHT)
observations =  Sex.fill(DOWN).is_not_blank().is_not_whitespace() - ts
Parentalstatus = cell.expand(DOWN).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(Parentalstatus,'Treatment group',DIRECTLY,LEFT),
            HDim(Clients,'Clients in treatment',CLOSEST,LEFT),
            HDimConst('Measure Type','count-of-new-presentations-to-treatment'),
            HDimConst('Unit','new-presentations-to-treatment'),
            HDimConst('Period', 'gregorian-interval/2017-04-01T00:00:00/P1Y'),
            HDim(Sex,'Basis of treatment',DIRECTLY,ABOVE)
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
if is_interactive():
        savepreviewhtml(c1)
# -

table = c1.topandas()

import numpy as np
table['OBS'].replace('', np.nan, inplace=True)
table.dropna(subset=['OBS'], inplace=True)
table.rename(columns={'OBS': 'Value'}, inplace=True)
table['Value'] = table['Value'].astype(int)
table['Value'] = table['Value'].map(lambda x:''
                                  if (x == '-')
                                  else int(x))

# +
# table = table[['Period','Basis of treatment','Treatment group','Clients in treatment','Measure Type','Value','Unit']]
# -

table.head()

table['treatment'] = table['Treatment group'] + ' - ' + table['Basis of treatment'] 

table['Basis of treatment'] = table['treatment'].map(
    lambda x: {
        'Parent living with children - F':'parental-status/parent-living-with-children-female',
        'Other contact living with children - F':'parental-status/other-contact-living-with-children-female',
        'Parents not with children - F':'parental-status/parents-not-with-children-female',
        'Not parent no contact with children - F':'parental-status/not-parent-no-contact-with-children-female',
        'Incomplete data - F':'parental-status/incomplete-data-female',
        'Total - F':'parental-status/total-female',
        'Parent living with children - M':'parental-status/parent-living-with-children-male',
        'Other contact living with children - M':'parental-status/other-contact-living-with-children-male',
        'Parents not with children - M':'parental-status/parents-not-with-children-male',
        'Not parent no contact with children - M':'parental-status/not-parent-no-contact-with-children-male',
        'Incomplete data - M':'parental-status/incomplete-data-male',
        'Total - M':'parental-status/total-male',
        'Total':'parental-status/total' }.get(x, x))

new_table = pd.concat([new_table, table])

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


