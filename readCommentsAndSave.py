import commentCompile
import os
import json
import pickle

"""Call this file to process saved json files into pickle files"""

DBList = dict()

jsonlist = dict() # lists the path and json file name for all files in ./r/
for path, dirs, files in os.walk("./r/"):
    for f in files:
        #print path + "/" + f
        if not path in jsonlist:
            jsonlist[path] = list()
        jsonlist[path].append(f)

for directory in jsonlist:
    if not directory in DBList:
        DBList[directory] = dict()
    for filename in jsonlist[directory]:
        commentCompile.parseJSON(DBList[directory], directory + "/" + filename)

for subreddit in DBList:
    save = open("DBs/" + subreddit[4:] + "_db.pickle", "w")
    pickle.dump(DBList[subreddit], save)
    save.close()
