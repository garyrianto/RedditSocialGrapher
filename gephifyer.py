import commentCompile
import sys
import pickle

"""Run this file to take a pickled database and extract one subreddit's data into a Gephi-compatible file"""


subreddit = "AskReddit"

path = "./r/" + subreddit

try:
    load = open("DBsave.pickle", "r")
    DB = pickle.load(load)
    load.close()
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)    
    quit()

archive = DB[path]

output = open(subreddit + ".csv", "w")

for person in archive:
        if (person == "[deleted]"):
            continue #skip [deleted]
        bufferstr = archive[person].ID + ","
        for repliedTo in archive[person].replies:  

            for x in range(0, archive[person].replies[repliedTo]): # append the number of times person replied to.
                bufferstr += repliedTo + ","
        bufferstr = bufferstr[:-1] # strip the trailing comma
        bufferstr += "\n"

        """ skips if the user only replied to one person, once """
        if len(bufferstr.split(",")) > 2:
            output.write(bufferstr) 
