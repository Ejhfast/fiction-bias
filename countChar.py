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
nlp = spacy.en.English()

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
catFemChar = defaultdict(int)
storyMaleChar = defaultdict(int)
catFemChar = defaultdict(int)
catMaleChar = defaultdict(int)
maleNames = Set([])
femaleNames = Set([])

def countChar(chapter, cat, storyid):
  for sen in chapter.split("." or "!" or "?"):
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
        if ((tk.lower not in maleNames) and names.ismalename(tk.lower_)):
           maleNames.add(tk.lower)
           storyMaleChar[storyid] += 1
           catMaleChar[cat]+= 1
        if((tk.lower not in femaleNames) and names.isfemalename(tk.lower_)):
           femaleNames.add(tk.lower)
           storyFemChar[storyid] += 1
           catFemChar[cat] += 1
        
    except UnicodeDecodeError:
      pass

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countChar(chapter, cat, storyid)

f = open("charcounts.txt", 'w')
genre = graph.getGenres()
for key in sorted(catFemChar):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + "," + "Female:" + str(catFemChar[key]) + "," + "Male:" + str(catMaleChar[key]) + "\n")  
f.close

f = open("charcountsstories.txt", 'w')
pickle.dump(storyFemChar, f)
pickle.dump(storyMaleChar, f)


