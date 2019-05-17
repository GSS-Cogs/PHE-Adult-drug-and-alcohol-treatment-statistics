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

# Table 6.2.1: Change in use of cited substance for clients with a review TOP/AOR in the year who reported using at the start of treatment

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

tab = loadxlstabs(inputFile, sheetids='Table 6.2.1')[0]

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('B7').expand(DOWN).expand(RIGHT).is_not_blank()
observations

reason = tab.excel_ref('A6').expand(DOWN).is_not_blank() 
reason

clients = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
clients

Treatmentstatus = tab.excel_ref('B3').expand(RIGHT).is_not_blank()
Treatmentstatus

MeasureType = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
MeasureType

Dimensions = [
            HDim(clients,'Clients in treatment',CLOSEST,LEFT),
            HDim(Treatmentstatus,'Treatment Status',CLOSEST,LEFT),
            HDim(reason,'Substance',DIRECTLY,LEFT),
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

new_table['Measure Type'].unique()

new_table['Measure Type'] = new_table['Measure Type'].map(
    lambda x: {
        'n' : 'Count', 
        '%' : 'Percentage'
        }.get(x, x))

new_table.tail()

new_table.dtypes

new_table['Value'] = new_table['Value'].astype(str)

new_table.head(3)

new_table['Treatment Status'] = new_table['Treatment Status'].map(
    lambda x: {
        'START OF TREATMENT' : 'Start of treatment',
        'AT SIX MONTH REVIEW' : 'At six month Review'
        }.get(x, x))

new_table.tail()

new_table = new_table[['Substance','Treatment Status','Clients in treatment','Measure Type','Value','Unit']]

if is_interactive():
    SubstancetinationFolder = Path('out')
    SubstancetinationFolder.mkdir(exist_ok=True, parents=True)
    new_table.to_csv(SubstancetinationFolder / ('table6.2.1.csv'), index = False)


