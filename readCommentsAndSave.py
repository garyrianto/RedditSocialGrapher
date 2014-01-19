import commentCompile
import os
import json
import pickle

"""Call this file to """

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
        parseJSON(DBList[directory], directory + "/" + filename)

save = open("DBsave.pickle", "w")
pickle.dump(DBList, save)
save.close()
