import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle
from sets import Set
import names
import graph

stories = {}
categories = {}
writers = {}
ratings = {}

f = open("/home/ubuntu/ebs/dataset/story_chapters/part-m-00000", "r")
for line in f:
  storyID, textID = [x.rstrip() for x in line.split("\t")]
  stories[textID] = storyID
f.close

f = open("/home/ubuntu/ebs/dataset/story_details/part-m-00000", "r")
for line in f:
  writerID, storyID, categoryID, rating = [x.rstrip() for x in line.split("\t")]
  categories[storyID] = categoryID
  writers[storyID] = writerID
  ratings[storyID] = rating
f.close

storyFemChar = defaultdict(int)
storyFemMain = defaultdict(int)

catFemChar = defaultdict(int)
catFemMain = defaultdict(int)

catMaleTopMain = defaultdict(int)
storyMaleTopMain = defaultdict(int)

storyMaleChar = defaultdict(int)
storyMaleMain = defaultdict(int)

catMaleChar = defaultdict(int)
catMaleMain = defaultdict(int)

catFemTopMain = defaultdict(int)
storyFemTopMain = defaultdict(int)

nameList = defaultdict(dict)

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

def countChar(chapter, cat, storyid):
  for tk in chapter.split(" "):
     if(tk.lower() in nameList[storyid]):
        nameList[storyid][tk.lower()] += 1
     else:
        if (names.ismalename(tk.lower())):
           nameList[storyid][tk.lower()] = 1
           storyMaleChar[storyid] += 1
           catMaleChar[cat]+= 1
        if(names.isfemalename(tk.lower())):
           nameList[storyid][tk.lower()] = 1
           storyFemChar[storyid] += 1
           catFemChar[cat] += 1

def getMain(nameList, storyid, cat, topMain):
  mainchar = keywithmaxval(nameList[storyid])
  print(mainchar)
  if(nameList[storyid][mainchar] == 0): return
  nameList[storyid][mainchar] = 0
  if(names.isfemalename(mainchar)):
     catFemMain[cat] += 1
     storyFemMain[storyid] += 1
     if(topMain == True):
        catFemTopMain[cat] += 1
        storyFemTopMain[storyid] += 1
  elif (names.ismalename(mainchar)):
     catMaleMain[cat] += 1
     storyMaleMain[storyid] += 1
     if(topMain == True):
        catMaleTopMain[cat] += 1
        storyMaleTopMain[storyid] += 1
  

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countChar(chapter, cat, storyid)

for storyid in storyFemChar:
  cat = int(categories[storyid])
  getMain(nameList, storyid, cat, True)
  getMain(nameList, storyid, cat, False)
  getMain(nameList, storyid, cat, False)

f = open("charcounts.txt", 'w')
genre = graph.getGenres()
for key in sorted(catFemChar):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + ", " + "Female:" + str(catFemChar[key]) + ", " + "Male:" + str(catMaleChar[key]) +  ", " + "Ratio:" + str(catFemChar[key]/float(catMaleChar[key])) + "\n")
   f.write("Top 3 Main, " + "Female:" + str(catFemMain[key]) + ", " + "Male:" + str(catMaleMain[key]) +  ", " + "Ratio:" + str(catFemMain[key]/float(catMaleMain[key])) + "\n")
   f.write("Top 1 Main, " + "Female:" + str(catFemTopMain[key]) + ", " + "Male:" + str(catMaleTopMain[key]) +  ", " + "Ratio:" + str(catFemTopMain[key]/float(catMaleTopMain[key])) + "\n")
   f.write("\n") 
f.close

f = open("charcountsstories.txt", 'w')
pickle.dump(storyFemChar, f)
pickle.dump(storyMaleChar, f)
pickle.dump(storyFemMain, f)
pickle.dump(storyMaleMain, f)
pickle.dump(storyFemTopMain, f)
pickle.dump(storyMaleTopMain, f)
pickle.dump(catFemChar, f)
pickle.dump(catMaleChar, f)
pickle.dump(catFemMain, f)
pickle.dump(catMaleMain, f)
pickle.dump(catFemTopMain, f)
pickle.dump(catMaleTopMain, f)
pickle.dump(nameList, f)



