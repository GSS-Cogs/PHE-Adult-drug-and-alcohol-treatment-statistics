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

# Table 4.12.3: Clients' children receiving early help or in contact with children's social care

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 4.12.3']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

cell = tab.filter("Help received or in contact with children's social care")
cell.assert_one()
obs = tab.filter('Missing').shift(0,-1).expand(RIGHT)
observations = tab.filter('n').fill(DOWN).is_not_blank().is_not_whitespace() - obs
helps = cell.expand(DOWN).is_not_blank().is_not_whitespace()
Clients = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(helps,'Treatment group',DIRECTLY,LEFT),
            HDim(Clients,'Clients in treatment',CLOSEST,LEFT),
            HDimConst('Measure Type','count-of-children'),
            HDimConst('Unit','children'),
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

new_table["Basis of treatment"] = new_table["Treatment group"].map(
    lambda x: {
        "Help received or in contact with children's social care":"help-received-or-in-contact-with-childrens-social-care",
        'Early help':'help-received-or-in-contact-with-childrens-social-care/early-help',
        'Child in need':'help-received-or-in-contact-with-childrens-social-care/child-in-need',
        'Child protection plan':'help-received-or-in-contact-with-childrens-social-care/child-protection-plan',
        'Looked after child':'help-received-or-in-contact-with-childrens-social-care/looked-after-child',
        'No early help':'help-received-or-in-contact-with-childrens-social-care/no-early-help',
        'Missing':'help-received-or-in-contact-with-childrens-social-care/missing',
        'Total':'help-received-or-in-contact-with-childrens-social-care/total'
        }.get(x, x))

new_table["Substance type"] = new_table['Clients in treatment'].map(
    lambda x: {
        'Opiates' : 'opiate', 
        'Non-opiates only' : 'non-opiate-only', 
        'Alcohol & non-opiates' : 'non-opiate-and-alcohol',
        'Alcohol only' : 'alcohol-only', 
        'Total' : 'total'
                }.get(x, x))

new_table = new_table[['Period','Basis of treatment','Substance type','Measure Type','Value','Unit']]

new_table


