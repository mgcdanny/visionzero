# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests as rq
import zipfile as zp
import StringIO
import os
import pandas as pd

# <codecell>

def makeTime():
    """Make all the links to the data we want. Data doesn't start until 2011_08"""
    year = ["2013","2012","2011"]
    month = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    container = []
    for y in year:
        for m in month:
            if (y != "2011") or (m not in ["01","02","03","04","05","06","07"]):
                container.append(y+"_"+m)
    return container

# <codecell>

dates = makeTime()

# <codecell>

for d in dates:
    try:
        r = rq.get("http://www.nyc.gov/html/nypd/downloads/zip/traffic_data/{}_acc.zip".format(d))
        z = zp.ZipFile(StringIO.StringIO(r.content))
        z.extractall(path="citycol/{}".format(d))
    except:
        print("this date does not have a file"+str(d))

# <codecell>

import glob

# <codecell>

a = glob.glob("citycol/*/*.xlsx")

# <codecell>

container = []
for f in glob.glob("citycol/*/*.xlsx"):
    #meta = f.split('\\')
    meta = f.split('/')
    date = meta[1]
    category = meta[2].split('acc')[0]
    container.append((f,date,category))

# <codecell>

df = pd.read_excel(container[0][0], "Table 1", index_col=None, skiprows=2, names=["intersection", "acc_count", "deleteMe", "person_involved_count", "acc_w_injury_count", "category", "injured", "killed", "vehicle_types", "factors"])

# <codecell>

df = df.drop('deleteMe', axis=1)

# <codecell>

import re
import numpy as np

# <codecell>

def getPrecinct(v):
    if isinstance(v, unicode):
        if re.match(r".*Precinct", v):
            return v
    else:
        return None

# <codecell>

df['precinct'] = df['intersection'].map(lambda x: getPrecinct(x))
df['precinct'] = df['precinct'].fillna(method='pad')

# <codecell>

df = df.dropna(how='all', subset=['acc_count','person_involved_count','acc_w_injury_count','category','injured','killed','vehicle_type','factors'])
df = df.dropna(how='all', subset=['acc_count'])
df = df[df.intersection != 'Intersection   Address']
df = df.reset_index()

# <codecell>


# <codecell>

injured_container = []
for itr, row in df.iterrows():
    temp = {'index': row['index']}
    if isinstance(row['injured'], unicode):
        injury_count = row['injured'].split('\n')
        if re.match(r'.*\n.*', row['category']):
            categories = row['category'].split('\n')
            temp.update(dict(zip(categories, injury_count)))
        else:
            categories = row['category'].split(' ')
            temp.update(dict(zip(categories, injury_count)))
    else:
        temp[row['category']] =  row['injured']
    injured_container.append(temp)
        

# <codecell>

test = pd.DataFrame(data=injured_container)

# <codecell>

test

# <codecell>

test.iloc[0:10]

# <codecell>

sum(map(int, injured))

# <codecell>

df['injured'].map(makeCols)

# <codecell>

df[~df['injured'].map(lambda x: isinstance(x, unicode))]

# <codecell>

df['injured'].map(makeCols)

# <codecell>

ckilled = [c+'_killed' for c in cols]
killed = ['killed'].split('\n')

# <codecell>

cols = df.iloc[7]['category'].split(' ')

# <codecell>

cinjured = [c+'_injured' for c in cols]

# <codecell>

injured = df.iloc[7]['injured'].split('\n')

# <codecell>

dict(zip(cinjured, injured))

# <codecell>

df.iloc[7]['killed'].split('\n')

# <codecell>

for index, row in df.iterrows():
    

# <codecell>

with open('allSummons.csv','wb') as f:
    for d in container:
        raw = pd.read_excel(d[0],"Table 1", skiprows=2, index_col=None, names=["type","mtd","ytd"])
        backSafely = {'type': raw.ix[0]['type'].split('\n')[1], 'mtd': raw.ix[0]['mtd'].split('\n')[1], 'ytd':raw.ix[1]['ytd']}
        otherMovers = {'type': raw.ix[34]['type'].split('\n')[0], 'mtd': raw.ix[34]['mtd'].split('\n')[0], 'ytd':raw.ix[34]['ytd']}
        totalMovers = {'type': raw.ix[34]['type'].split('\n')[1], 'mtd': raw.ix[34]['mtd'].split('\n')[1], 'ytd':raw.ix[35]['ytd']}
        df = raw[2:34]
        df = df.append([backSafely, otherMovers, totalMovers], ignore_index=True)
        df['location'] = d[2]
        df['date'] = d[1]
        df['year'] = df['date'].apply(lambda x: x.split('_')[0])
        df['month'] = df['date'].apply(lambda x: x.split('_')[1])
        df.to_csv(f, header=False, index=False)

# <codecell>

raw = pd.read_csv("allSummons.csv", index_col=None, names=["type","mtd","ytd","location","date","year","month"])

# <codecell>

copMeta = pd.read_csv()

# <codecell>

raw.to_csv("allSummons_Headers.csv", index=False)

# <codecell>


