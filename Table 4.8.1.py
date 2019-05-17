# -*- coding: utf-8 -*-
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

# Table 4.8.1: Source of referral into treatment, new presentations to treatment

# +
from gssutils import *

if is_interactive():
    scraper = Scraper('https://www.gov.uk/government/collections/alcohol-and-drug-misuse-and-treatment-statistics')
    scraper.select_dataset(title=lambda x: x.startswith('Substance misuse treatment for adults'), latest=True)
    tabs = {tab.name: tab for tab in scraper.distribution(title=lambda x: x.startswith('Data tables')).as_databaker()}
# -

tab = tabs['Table 4.8.1']

# https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/752515/AdultSubstanceMisuseNDTMSDataTables2017-18.xlsx

cell = tab.filter('Referral Source')
cell.assert_one()
obs = tab.filter('Inconsistent/missing').shift(0,1).expand(RIGHT) | tab.filter('Other YP').shift(0,-1).expand(RIGHT)
observations = tab.filter('n').fill(DOWN).is_not_blank().is_not_whitespace() - obs
ReferralSource = cell.expand(DOWN).is_not_blank().is_not_whitespace() | \
                  cell.shift(1,0).expand(DOWN).is_not_blank().is_not_whitespace()
Clients = cell.expand(RIGHT).is_not_blank().is_not_whitespace()
Dimensions = [
            HDim(ReferralSource,'Treatment group',DIRECTLY,LEFT),
            HDim(Clients,'Clients in treatment',CLOSEST,LEFT),
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

new_table['Treatment group'].unique()

new_table['Basis of treatment'] = new_table['Treatment group'].map(
    lambda x: {
        'Referral Source':'referral-source',
        'Self, family and friends subtotal':'self-family-and-friends-subtotal',
        'Self':'self-family-and-friends-subtotal/self',
        'Other family and friends':'self-family-and-friends-subtotal/other-family-and-friends',
        'Health services and social care subtotal':'health-services-and-social-care-subtotal',
        'GP':'health-services-and-social-care-subtotal/gp',
        'Hospital':'health-services-and-social-care-subtotal/hospital',
        'Social services':'health-services-and-social-care-subtotal/social-services',
        'Health – other':'health-services-and-social-care-subtotal/health-other',
        'Other community health':'health-services-and-social-care-subtotal/health-other/other-community-health',
        'Psychiatry':'health-services-and-social-care-subtotal/health-other/psychiatry',
        'A&E':'health-services-and-social-care-subtotal/health-other/a-and-e',
        'Syringe Exchange':'health-services-and-social-care-subtotal/health-other/syringe-exchange',
        'Community care assessment':'health-services-and-social-care-subtotal/health-other/community-care-assessment',
        'Children social services':'health-services-and-social-care-subtotal/health-other/children-social-services',
        'Criminal justice subtotal':'criminal-justice-subtotal',
        'Arrest referral/DIP':'criminal-justice-subtotal/arrest-referral/dip',
        'Prison':'criminal-justice-subtotal/prison',
        'Probation':'criminal-justice-subtotal/probation',
        'Criminal justice – other':'criminal-justice-subtotal/criminal-justice-other',
        'ATR':'criminal-justice-subtotal/criminal-justice-other/atr',
        'DRR':'criminal-justice-subtotal/criminal-justice-other/drr',
        'Community rehabilitation company':'criminal-justice-subtotal/criminal-justice-other/community-rehabilitation-company',
        'Liaison and diversion':'criminal-justice-subtotal/criminal-justice-other/liaison-and-diversion',
        'Other criminal justice':'criminal-justice-subtotal/criminal-justice-other/other-criminal-justice',
        'Substance misuse service subtotal':'substance-misuse-service-subtotal',
        'Drug service statutory':'substance-misuse-service-subtotal/drug-service-statutory',
        'Drug service non-statutory':'substance-misuse-service-subtotal/drug-service-non-statutory',
        'Community alcohol team':'substance-misuse-service-subtotal/community-alcohol-team',
        'Other subtotal':'other-subtotal',
        'Other':'other-subtotal/other',
        'Other':'other-subtotal/other/other',
        'Other YP':'other-subtotal/other/other-yp',
        'Job centre plus':'other-subtotal/other/job-centre-plus',
        'Employment service':'other-subtotal/other/employment-service',
        'Other sex worker project':'other-subtotal/other/other-sex-worker-project',
        'Other treatment provider':'other-subtotal/other/other-treatment-provider',
        'Connexions':'other-subtotal/other/connexions',
        'Education service':'other-subtotal/other/education-service',
        'LAC':'other-subtotal/other/lac',
        'Employer':'other-subtotal/other/employer',
        'Other helplines & websites':'other-subtotal/other/other-helplines-and-websites',
        'Inconsistent/missing':'inconsistent/missing',
        'Total':'total'        
        }.get(x, x))

import urllib.request as request
import csv
import io
import requests
vrl="https://raw.githubusercontent.com/ONS-OpenData/ref_alcohol/master/codelists/substance-type.csv"
t=requests.get(vrl).content
g=pd.read_csv(io.StringIO(t.decode('utf-8')))
new_table = pd.merge(new_table, g, how = 'left', left_on = 'Clients in treatment', right_on = 'Label')
new_table.columns = ['Substance type' if x=='Notation' else x for x in new_table.columns]
new_table = new_table[['Period','Basis of treatment','Substance type','Measure Type','Value','Unit']]

new_table

new_table['Basis of treatment'].unique()


