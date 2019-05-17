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

# Table 4.9.2: Age and presenting substance of new presentations to treatment

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 4.9.2']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

cell = tab.filter('Substance')
cell.assert_one()
observations = tab.filter('n').fill(DOWN).is_not_blank().is_not_whitespace()
Substance = cell.expand(DOWN).is_not_blank().is_not_whitespace()
age = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(age,'Treatment group',DIRECTLY,ABOVE),
            HDim(Substance,'Clients in treatment',DIRECTLY, LEFT),
            HDimConst('Measure Type','count-of-new-presentations-to-treatment'),
            HDimConst('Unit','new-presentations-to-treatment'),
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

new_table['Basis of treatment'] = new_table['Treatment group'].map(
    lambda x: {
        '18-19':'age/18-19',
        '65+':'age/65plus',
        'Age':'age',
        '18':'age/18',
        '19':'age/19',
        '20-24':'age/20-24',
        '25-29':'age/25-29',
        '30-34':'age/30-34',
        '35-39':'age/35-39',
        '40-44':'age/40-44',
        '45-49':'age/45-49',
        '50-54':'age/50-54',
        '55-59':'age/55-59',
        '60-64':'age/60-64',
        '65-69':'age/65-69',
        '70+':'age/70plus',
        'Total':'age/total'}.get(x, x))

new_table['Clients in treatment'] = new_table['Clients in treatment'].str.rstrip('*')

new_table['Substance type'] = new_table['Clients in treatment'].map(
    lambda x: {
        'Opiate (not crack cocaine)':'opiate-not-crack-cocaine',
        'Both opiate and crack cocaine':'both-opiate-and-crack-cocaine',
        'Crack cocaine (not opiate)':'crack-cocaine-not-opiate',
        'Cannabis':'cannabis',
        'Cocaine':'cocaine',
        'Benzodiazepine':'benzodiazepine',
        'Amphetamine (other than ecstasy)':'amphetamine',
        'Other':'other',
        'Hallucinogen':'hallucinogen',
        'Other prescription drug':'other-prescription-drug',
        'Anti-depressant':'anti-depressant',
        'Solvent':'solvent',
        'Major tranquiliser':'major-tranquiliser',
        'Barbiturate':'barbiturate',
        'Alcohol':'alcohol-only',
        'Total number of individuals':'total'
        }.get(x, x))

new_table = new_table[['Period','Basis of treatment','Substance type','Measure Type','Value','Unit']]

new_table


