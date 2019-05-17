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

# Table 6.2.2: Number and proportion of individuals who were smoking at the start of treatment and referred for smoking cessation interventions

# +
from gssutils import *

if is_interactive():
    import requests
    from cachecontrol import CacheControl
    from cachecontrol.caches.file_cache import FileCache
    from cachecontrol.heuristics import LastModified
    from pathlib import Path

    session = CacheControl(requests.Session(),
                           cache=FileCache('.cache'),
                           heuristic=LastModified())

    sourceFolder = Path('in')
    sourceFolder.mkdir(exist_ok=True)

    inputURL = 'https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx'
    inputFile = sourceFolder / 'AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx'
    response = session.get(inputURL)
    with open(inputFile, 'wb') as f:
      f.write(response.content)    
# -

tab = loadxlstabs(inputFile, sheetids='Table 6.2.2')[0]

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('B4').expand(DOWN).expand(RIGHT).is_not_blank()
observations

substance = tab.excel_ref('A4').expand(DOWN).is_not_blank() 
substance

clients = tab.excel_ref('B3').expand(RIGHT).is_not_blank()
clients

Dimensions = [
            HDim(clients,'Clients in treatment',CLOSEST,LEFT),
            HDim(substance,'Substance',DIRECTLY,LEFT),
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


# +
def user_perc(x):
    
    if str(x) == '%':
        return 'Percentage'
    else:
        return 'Count'
    
new_table['Measure Type'] = new_table.apply(lambda row: user_perc(row['Clients in treatment']), axis = 1)

# -

new_table['Clients in treatment'] = new_table['Clients in treatment'].map(
    lambda x: {
        '%' : 'Percentage of clients received smoking cessation'
        }.get(x, x))

new_table.tail()

new_table.dtypes

new_table['Value'] = new_table['Value'].astype(str)

new_table.head(3)

new_table.tail()

new_table = new_table[['Substance','Clients in treatment','Measure Type','Value','Unit']]

if is_interactive():
    SubstancetinationFolder = Path('out')
    SubstancetinationFolder.mkdir(exist_ok=True, parents=True)
    new_table.to_csv(SubstancetinationFolder / ('table6.2.2.csv'), index = False)


