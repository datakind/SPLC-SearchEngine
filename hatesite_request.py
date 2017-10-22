# written by FBB @fedhere 10/21/2017
# reads SPLC list of "hate sites" and tries to access site w python requests. 
# logs result in hatesites_failures.log and hatesites_nonfailures.log

from __future__ import print_function
import requests
import pandas as pd

#running a safe request to get a response object and setting the status to -1
result = requests.get("http://cosmo.nyu.edu")
tmp = pd.read_csv("hatesitesDB.csv")
ffails = open("hatesite_failures.log", "w")
fexceptions = open("hatesite_exceptions.log", "w")
fsuccess = open("hatesite_nonfailures.log", "w")

for i,w in enumerate(tmp.Website.values):
#    print (i, w)
    result.status_code = -1
    if w.startswith("http://"): 
        try :
            result = requests.get(w)
        except requests.exceptions.ConnectionError:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "ConnectionError", file=fexceptions)
        except requests.exceptions.TooManyRedirects:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "TooManyRedirects", file=fexceptions)
    else: 
        #print ("add http")
        try: 
            result = requests.get("http://" + w)
        except requests.exceptions.ConnectionError:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "ConnectionError", file=fexceptions)
        except requests.exceptions.TooManyRedirects:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "TooManyRedirects", file=fexceptions)
        if not result.status_code == requests.codes.ok:
            #print ("add https")
            try:
                result = requests.get("https://" + w)
            except requests.exceptions.ConnectionError:
                print("%d issue with "%i, tmp.iloc[i].Group, w, "ConnectionError", file=fexceptions)
            except requests.exceptions.TooManyRedirects:
                print("%d issue with "%i, tmp.iloc[i].Group, w, "TooManyRedirects", file=fexceptions)
    if result.status_code == requests.codes.ok:
        print("%d NO ISSUES "%i, tmp.iloc[i].Group, w, , file=fsuccess)
        continue
    print("%d issue with "%i , tmp.iloc[i].Group, w, result.status_code, file=ffails)
