import json
import os

class Person:
    def __init__(self, ID):
        self.ID = ID
        self.replies = dict()
    
    def addReply(self, repliedTo):
        if repliedTo in self.replies:
            self.replies[repliedTo] += 1
        else:
            self.replies[repliedTo] = 1

    def __str__(self):
        str = "/u/%s replied to:" % (self.ID)
        for k in self.replies:
            str += "\n    /u/%s : %d" % (k, self.replies[k])
        return str

def readComment(DB, tree, author): 
# The author is the  person who the 'current' person replied to;
# that is, this function adds a reply to all the children of that comment
    for reply in tree:
        if not reply["kind"] == "t1":
            continue
        current = reply["data"]["author"]
        if not current in DB:
            DB[current] = Person(current)
        DB[current].addReply(author)
        if len(reply["data"]["replies"]) > 0:
            readComment(DB, reply["data"]["replies"]["data"]["children"], current)
        
def parseJSON(DB, filename):
    with open(filename, 'r') as jsonfile:
        rawdata = jsonfile.read()
    data = json.loads(rawdata)

    OP = data[0]["data"]["children"][0]["data"]["author"]

    for rep in data[1]["data"]["children"]:
        if not rep["kind"] == "t1" or rep["kind"] == "Listing":
            continue
        author = rep["data"]["author"]
        if not author in replyDB:
            replyDB[author] = Person(author)
        replyDB[author].addReply(OP)
        if len(rep["data"]["replies"]) > 0:
            replies = rep["data"]["replies"]["data"]["children"]
            readComment(replyDB, replies, rep["data"]["author"])
    
replyDB = dict()



jsonlist = dict() # lists the path and json file name for all files in ./r/
for path, dirs, files in os.walk("./r/"):
    for f in files:
        #print path + "/" + f
        if not path in jsonlist:
            jsonlist[path] = list()
        jsonlist[path].append(f)

quit()

path = 'r/askscience/'
for filename in filelist:
    parseJSON(replyDB, path + filename)

for p in replyDB:
    print replyDB[p]
