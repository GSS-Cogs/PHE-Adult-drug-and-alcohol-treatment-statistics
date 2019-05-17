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

# Table 5.1.1: Waiting times, first and subsequent interventions

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 5.1.1']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('C6').expand(DOWN).expand(RIGHT).is_not_blank()
observations

Source = tab.excel_ref('A6').expand(DOWN).is_not_blank()
Source

intervention = tab.excel_ref('B3').expand(RIGHT).is_not_blank()
intervention

Waitingtimes = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
Waitingtimes

MeasureType = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
MeasureType

Dimensions = [
            HDim(Source,'Substance',DIRECTLY,LEFT),
            HDim(intervention,'Intervention',CLOSEST,LEFT),
            HDim(Waitingtimes,'Waiting time',CLOSEST,LEFT),
            HDim(MeasureType,'Measure Type',DIRECTLY,ABOVE),
            HDimConst('Unit','People')            
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
# if is_interactive():
#     savepreviewhtml(c1)

new_table = c1.topandas()
new_table

new_table = new_table[new_table['OBS'] != 0 ]

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table.head()

new_table['Measure Type'] = new_table['Measure Type'].map(
    lambda x: {
        'n' : 'Count', 
        '%' : 'Percentage',
        }.get(x, x))

new_table.tail()

new_table.dtypes

new_table['Value'] = new_table['Value'].astype(str)

new_table.head(3)

new_table['Substance'] = new_table['Substance'].map(
    lambda x: {
        'Total' : 'All' 
        }.get(x, x))

new_table.head(3)

new_table = new_table[['Substance','Intervention','Waiting time','Measure Type','Value','Unit']]


