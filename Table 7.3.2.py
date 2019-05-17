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

# Table 7.3.2: Trends in the proportion of new presentations with housing problems, by NPS and all clients

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

tab = loadxlstabs(inputFile, sheetids='Table 7.3.2')[0]

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('B6').expand(DOWN).expand(RIGHT).is_not_blank()
observations

house = tab.excel_ref('A6').expand(DOWN).is_not_blank() - tab.excel_ref('A12').expand(DOWN)
house

Clients = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
Clients

period = tab.excel_ref('B3').expand(RIGHT).is_not_blank()
period

MeasureType = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
MeasureType

Dimensions = [
            HDim(house,'Housing Status',DIRECTLY,LEFT),
            HDim(Clients,'Clients in new treatment',CLOSEST,LEFT),
            HDim(MeasureType,'Measure Type',DIRECTLY,ABOVE),
            HDim(period,'Period',CLOSEST,LEFT),
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

new_table['Housing Status'] = new_table['Housing Status'].map(
    lambda x: {
        'Total' : 'All' 
        }.get(x, x))


# +
def user_perc(x):
    
    if x == None:
        return 'All inclusice Not stated/missing'
    else:
        return x
    
new_table['Housing Status'] = new_table.apply(lambda row: user_perc(row['Housing Status']), axis = 1)
# -

new_table.head(3)

new_table = new_table[['Period','Housing Status','Clients in new treatment','Measure Type','Value','Unit']]

if is_interactive():
    SubstancetinationFolder = Path('out')
    SubstancetinationFolder.mkdir(exist_ok=True, parents=True)
    new_table.to_csv(SubstancetinationFolder / ('table7.3.2.csv'), index = False)


