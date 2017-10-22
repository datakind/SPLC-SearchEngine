from __future__ import print_function
import requests
import pandas as pd

#running a safe request to get a response object and setting the status to -1
result = requests.get("http://cosmo.nyu.edu")
tmp = pd.read_csv("hatesitesDB.csv")

for i,w in enumerate(tmp.Website.values):
#    print (i, w)
    result.status_code = -1
    if w.startswith("http://"): 
        try :
            result = requests.get(w)
        except requests.exceptions.ConnectionError:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "ConnectionError")
        except requests.exceptions.TooManyRedirects:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "TooManyRedirects")
    else: 
        #print ("add http")
        try: 
            result = requests.get("http://" + w)
        except requests.exceptions.ConnectionError:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "ConnectionError")
        except requests.exceptions.TooManyRedirects:
            print("%d issue with "%i, tmp.iloc[i].Group, w, "TooManyRedirects")
        if not result.status_code == requests.codes.ok:
            #print ("add https")
            try:
                result = requests.get("https://" + w)
            except requests.exceptions.ConnectionError:
                print("%d issue with "%i, tmp.iloc[i].Group, w, "ConnectionError")
            except requests.exceptions.TooManyRedirects:
                print("%d issue with "%i, tmp.iloc[i].Group, w, "TooManyRedirects")
    if result.status_code == requests.codes.ok:
        print("%d NO ISSUES "%i, tmp.iloc[i].Group, w)
        continue
    print("%d issue with "%i , tmp.iloc[i].Group, w, result.status_code)
