# written by FBB @fedhere 10/21/2017
# reads output of hatesite_requests.py and counts sites that failed as fraction of ideology

import numpy as np
import pandas as pd

f = open("hatesite_failures.log")
failures = f.readlines()
fails = [f.split(" ")[-2] for f in failures[:-1]]

tmp = pd.read_csv("hatesitesDB.csv")

ideologies = tmp.Ideology.drop_duplicates()
ideologycount = {}
for id in ideologies:
    ideologycount[id] = [0, (tmp.Ideology.values == id).sum()]

tmp = tmp.sort("Ideology")

for i,t in enumerate(tmp.Website.values):
    (ideologycount[tmp.iloc[i].Ideology])[0] += (np.array([t in f for f in fails]).sum() > 0)

for id in ideologycount:
    print "%s, %d, %d"%(id, ideologycount[id][0] * 1.0 / ideologycount[id][1] * 100, ideologycount[id][1])

