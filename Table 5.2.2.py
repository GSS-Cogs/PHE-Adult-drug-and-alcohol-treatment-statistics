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

# Table 5.2.2: Interventions received by clients in treatment, new interventions

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 5.2.2']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('C6').expand(DOWN).expand(RIGHT).is_not_blank()
observations

Substance = tab.excel_ref('A6').expand(DOWN).is_not_blank() 
Substance

Setting = tab.excel_ref('B3').expand(DOWN).is_not_blank()
Setting

MeasureType = tab.excel_ref('C5').expand(RIGHT).is_not_blank()
MeasureType

Intervention = tab.excel_ref('C4').expand(RIGHT).is_not_blank()
Intervention

Dimensions = [
            HDim(Substance,'Substance',CLOSEST,ABOVE),
            HDim(Setting,'Setting',DIRECTLY,LEFT),
            HDim(Intervention,'Clients in Treatment',CLOSEST,LEFT),
            HDim(MeasureType,'Measure Type',DIRECTLY,ABOVE),
            HDimConst('Unit','People')            
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
# if is_interactive():
#     savepreviewhtml(c1)

new_table = c1.topandas()
new_table

new_table = new_table[new_table['OBS'] != 0 ]

new_table = new_table[new_table['OBS'] != '' ]

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table['Clients in Treatment'] = new_table['Clients in Treatment'] + ' intervention'

new_table.head()

new_table['Measure Type'].unique()

new_table['Measure Type'] = new_table['Measure Type'].map(
    lambda x: {
        'n' : 'Count', 
        '%' : 'Percentage',
        None : 'Count'
        }.get(x, x))

new_table.tail()

new_table.dtypes

new_table['Value'] = new_table['Value'].astype(str)

new_table.head(3)

new_table['Substance'] = new_table['Substance'].map(
    lambda x: {
        'Total' : 'All' 
        }.get(x, x))

new_table['Setting'] = new_table['Setting'].map(
    lambda x: {
        'Total*' : 'All' 
        }.get(x, x))

new_table.tail()

new_table = new_table[['Substance','Setting','Clients in Treatment','Measure Type','Value','Unit']]


