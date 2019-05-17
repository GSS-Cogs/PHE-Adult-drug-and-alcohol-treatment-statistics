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

# AdultSubstanceMisuseNDTMSDataTables2017-18

# Data from 4 series compiled here for review other series, 5,6,7,8 need to be updated based on review comments, updated in trello

from gssutils import *
scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
scraper

scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
scraper

tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
tabs.keys()


# +
# %%capture

def process_tab(t):
    %run "$t"
    return new_table

observations = pd.concat(
    process_tab(f'{t}.ipynb') for t in tabs.keys() if t.startswith('Table 4')
)
# -

observations['Measure Type'] = observations['Measure Type'].map(
    lambda x: {
        'count-of-clients-in-treatment' : 'Count of clients in treatment',
       'count-of-new-presentations-to-treatment' :'Count of new presentations to treatment',
        'count-of-children' : 'Count of children'
        }.get(x, x))

out = Path('out')
out.mkdir(exist_ok=True, parents=True)
observations.drop_duplicates().to_csv(out / 'observations.csv', index=False)

from gssutils.metadata import THEME
scraper.dataset.family = 'health'
scraper.dataset.theme = THEME['health-social-care']
with open(out / 'dataset.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())
