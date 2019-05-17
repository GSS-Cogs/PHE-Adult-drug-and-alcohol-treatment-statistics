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

# Table 5.2.3: Total individuals in settings (overlap between 5.2.1 and 5.2.2)

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 5.2.3']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('B5').expand(DOWN).expand(RIGHT).is_not_blank()
observations

Setting = tab.excel_ref('A5').expand(DOWN).is_not_blank()
Setting

Dimensions = [
            HDimConst('Substance','All'),
            HDim(Setting,'Setting',DIRECTLY,LEFT),
            HDimConst('Clients in Treatment','All'),
            HDimConst('MeasureType','Count'),
            HDimConst('Unit','People')            
            ]

c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
# if is_interactive():
#     savepreviewhtml(c1)

new_table = c1.topandas()
new_table

new_table.columns = ['Value' if x=='OBS' else x for x in new_table.columns]

new_table.head()

new_table.dtypes

new_table['Value'] = new_table['Value'].astype(str)

new_table.head(3)

new_table = new_table[['Substance','Setting','Clients in Treatment','Measure Type','Value','Unit']]


