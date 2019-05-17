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

# Appendix B: Thirteen-year treatment population first presentation and treatment contact status at 31 March 2018

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

tab = loadxlstabs(inputFile, sheetids='Appendix B')[0]

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

observations = tab.excel_ref('B5').expand(DOWN).expand(RIGHT).is_not_blank()
observations = observations - tab.excel_ref('B').expand(DOWN).expand(RIGHT).by_index([12,20,28,36])
observations

clients = tab.excel_ref('A').expand(DOWN).by_index([3,11,19,27,35])
clients

treatmentstatus = tab.excel_ref('A5').expand(DOWN).is_not_blank() - clients
treatmentstatus

period = tab.excel_ref('B4').expand(RIGHT).is_not_blank() 
period

Dimensions = [
            HDim(clients,'Clients in treatment',CLOSEST,ABOVE),
            HDimConst('Measure Type','Count'),
            HDim(treatmentstatus, 'Treatment Status',DIRECTLY,LEFT),
            HDim(period, 'Period',DIRECTLY,ABOVE),
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

new_table.tail()

new_table.dtypes

new_table['Value'] = new_table['Value'].astype(str)

new_table.head(3)


# +
def user_perc(x,y):
    
    if str(x) == '%':
        return 'Percentage'
    else:
        return y
    
new_table['Measure Type'] = new_table.apply(lambda row: user_perc(row['Period'],row['Measure Type']), axis = 1)

# -

new_table['Period'] = new_table['Period'].map(
    lambda x: {
        'Total' : 'All years',
        '%'     : 'All years'
        }.get(x, x))

new_table.tail()

new_table = new_table[['Period','Treatment Status','Clients in treatment','Measure Type','Value','Unit']]

if is_interactive():
    SubstancetinationFolder = Path('out')
    SubstancetinationFolder.mkdir(exist_ok=True, parents=True)
    new_table.to_csv(SubstancetinationFolder / ('Appendix B.csv'), index = False)


