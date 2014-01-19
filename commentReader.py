import requests
import json
import re
import os
import time

headers = {
            'User-Agent': "'Comment social graph data collector' by /u/Corticotropin"
          }

unneededFields = ["subreddit_id", "banned_by", "subreddit", "saved", "id", "parent_id", "approved_by", "edited", "author_flair_css_class", "body_html", "link_id", "score_hidden", "name", "created", "author_flair_text", "distinguished", "num_reports"]

reddits = ["mildlyinteresting", "worldnews", "askreddit", "todayilearned", "explainlikeimfive", "askscience", "programming"]

cwd = os.getcwd() #"current working directory"

def removeUnneededFieldsFromData(comment):
    if comment["kind"] == "t1":
        for f in unneededFields:
            if f in comment["data"]:
                del comment["data"][f]
        if "replies" in comment["data"] and len(comment["data"]['replies']) > 0:
            for c in comment["data"]['replies']["data"]["children"]:
                removeUnneededFieldsFromData(c)
    elif comment["kind"] == "more":
        del comment["data"]


def stripAndSave(link):
    starttime = time.time()
    url = r'http://www.reddit.com%s.json' % (link[:-1])
    raw = requests.get(url, headers=headers)
    data = raw.json()
    subreddit = data[0]["data"]["children"][0]["data"]["subreddit"]
    title = data[0]["data"]["children"][0]["data"]["permalink"]
    # Extract the unique part of the Reddit URL, ie the parts after 'comment/'
    m = re.search('comments/([\w\d]+/[\w+]+)', title) 
    title = m.group(1)
    title = re.sub('/', ':', title)
    filename = "r/" + subreddit + "/" + title + ".json"
    for child in data[1]["data"]["children"]:
       removeUnneededFieldsFromData(child) # strip the irrelevant cruft from the json files, halving their storage space
    if not os.path.isdir(cwd + "/" + subreddit):
        try:
            os.makedirs("r/" + subreddit + "/")
        except OSError, e:
            if e.errno != 17: # This error is simply signalling that the directories exist already. Therefore, ignore it
                raise #if it's a different error, "raise" another error
    f = open(filename, "w")
    f.write(json.dumps(data))
    f.close()
    endtime = time.time()
    if endtime - starttime < 2:
        time.sleep(2 - (endtime - starttime))
    

"""print "started"
stripAndSave(r'/r/todayilearned/comments/1vexzs/til_when_ignored_by_that_person_whose_attention.json')

quit()"""

loopstart = time.time()
for reddit in reddits:
    print "Reading from subreddit /r/%s" % (reddit)
    r = requests.get(r'http://www.reddit.com/r/%s/hot.json?limit=100' % (reddit), headers = headers)
    data = r.json()

    # A list of reddit Thing objects that are posts.
    postedThings = data["data"]["children"]
    counter = 1;
    for thing in postedThings:
        if not thing["data"]["stickied"] == 1: 
            print str(counter) + ": " + thing["data"]["title"]
            counter += 1
            stripAndSave(thing["data"]["permalink"])
loopend = time.time()

print str(loopend - loopstart) + " seconds elapsed, total"