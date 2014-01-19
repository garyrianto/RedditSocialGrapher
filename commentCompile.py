import json
import os

""" This module defines methods and a class to take a Reddit archive and create a representation of who replied to whom."""




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

"""A recursive function that traverses the comment tree"""
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
        

"""This is the function to call. 
DB is a dict() of People. filename is a string that represents a path to the json file. parseJSON() must be called once for each json file."""
def parseJSON(DB, filename):
    with open(filename, 'r') as jsonfile:
        rawdata = jsonfile.read()
    data = json.loads(rawdata)

    OP = data[0]["data"]["children"][0]["data"]["author"]

    for rep in data[1]["data"]["children"]:
        if not rep["kind"] == "t1" or rep["kind"] == "Listing":
            continue
        author = rep["data"]["author"]
        if not author in DB:
            DB[author] = Person(author)
        DB[author].addReply(OP)
        if len(rep["data"]["replies"]) > 0:
            replies = rep["data"]["replies"]["data"]["children"]
            readComment(DB, replies, rep["data"]["author"])
