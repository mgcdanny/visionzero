# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

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
    r = rq.get("http://www.nyc.gov/html/nypd/downloads/zip/traffic_data/{}_sum.zip".format(d))
    z = zp.ZipFile(StringIO.StringIO(r.content))
    z.extract("citysum.xlsx", path="citysum/")
    os.rename("citysum/citysum.xlsx","citysum/citysum{}.xlsx".format(d))

# <codecell>

with open('citySummons.csv','wb') as f:
    for d in dates:
        raw = pd.read_excel("citysum/citysum{}.xlsx".format(d),0, skiprows=2, index_col=None, names=["type","mtd","ytd"])
        backSafely = {'type': raw.ix[0]['type'].split('\n')[1], 'mtd': raw.ix[0]['mtd'].split('\n')[1], 'ytd':raw.ix[1]['ytd']}
        otherMovers = {'type': raw.ix[34]['type'].split('\n')[0], 'mtd': raw.ix[34]['mtd'].split('\n')[0], 'ytd':raw.ix[34]['ytd']}
        totalMovers = {'type': raw.ix[34]['type'].split('\n')[1], 'mtd': raw.ix[34]['mtd'].split('\n')[1], 'ytd':raw.ix[35]['ytd']}
        df = raw[2:34]
        df = df.append([backSafely, otherMovers, totalMovers], ignore_index=True)
        df['date'] = d
        df.to_csv(f, header=False, index=False)

# <codecell>


