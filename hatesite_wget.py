# written by FBB @fedhere 10/21/2017
# reads SPLC list of "hate sites" and tries to access site w wget. 
# saves content into a file in a directory by the name of the website

import pandas as pd
import os

tmp = pd.read_csv("hatesitesDB.csv")

for i in tmp.index:
    #skip if name is missing
    if isinstance(tmp.iloc[i].Website, float):
        continue
    #directory name where html is stored is inherited by the website 
    #parsing the group name is too complicated
    dirname = str(tmp.iloc[i].Website.replace("http://","").replace("https://","").replace("/","").replace(".",""))
    #create directory
    os.system('mkdir ' + dirname)
    #moving to that dir
    os.chdir(dirname)
    #getting all html of main page
    os.system("wget " + tmp.iloc[i].Website)
    #back to the project dir
    os.chdir("/home/fb55/hateSitesCrawler")
