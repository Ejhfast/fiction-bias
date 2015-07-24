import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle
from passactdata import verbs
import names
import graph

stories = {}
f = open("/home/ubuntu/ebs/dataset/story_chapters/part-m-00000", "r")
for line in f:
  storyID, textID = [x.rstrip() for x in line.split("\t")]
  stories[textID] = storyID
f.close

categories = {}
writers = {}
ratings = {}
f = open("/home/ubuntu/ebs/dataset/story_details/part-m-00000", "r")
for line in f:
  writerID, storyID, categoryID, rating = [x.rstrip() for x in line.split("\t")]
  categories[storyID] = categoryID
  writers[storyID] = writerID
  ratings[storyID] = rating
f.close

nlp = spacy.en.English()

class Cat:
  def __init__(self):
     self.actFem = 0
     self.passFem = 0
     self.actMal = 0
     self.passMal = 0

cats = {}
for x in range (0, 25):
  cats[x] = Cat()

def countVerbs(chapter, cat):
  for sen in chapter.split("." or "!" or "?"):
#    if(cats[cat].count >= N and rats[rat].count >=N): return
#    if(cats[cat].count < N):
#       cats[cat].count += 1
#    if(rats[rat].count < N):
#       rats[rat].count += 1
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
            
        if(tk.pos_ == "VERB" and tk.lemma_ in verbs and verbs[tk.lemma_] != 'n'):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "she" or names.isfemalename(x.lower_)):
                   if(verbs[tk.lemma_] == 'a'):
                      cats[cat].actFem += 1
                   else:
                      cats[cat].passFem += 1
                elif (x.lower_ == "he" or names.ismalename(x.lower_)):
                   if(verbs[tk.lemma_] == 'a'):
                      cats[cat].actMal += 1
                   else:
                      cats[cat].passMal += 1
    except UnicodeDecodeError:
      pass

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countVerbs(chapter, cat)
  
f = open("passact.txt", 'w')
genre = graph.getGenres()
for key in sorted(cats):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + ", " + "Female active: " + str(cats[key].actFem) + ", " + "Female passive: " + str(cats[key].passFem) + "\n")
   if(cats[key].actFem != 0): f.write("Ratio:" + str(cats[key].passFem/float(cats[key].actFem)) + "\n")
   f.write(gen + ", " + "Male active: " + str(cats[key].actMal) + ", " + "Male passive: " + str(cats[key].passMal) +  "\n")
   if(cats[key].actMal != 0): f.write("Ratio:" + str(cats[key].passMal/float(cats[key].actMal)) + "\n")
   f.write("\n") 
f.close
