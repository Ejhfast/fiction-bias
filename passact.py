import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle
from passactdata import verbs
import names
import graph

N = 100000

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
     self.count = 0

cats = {}
for x in range (0, 25):
  cats[x] = Cat()

def countVerbs(chapter, cat):
  for sen in chapter.split("." or "!" or "?"):
    if(cats[cat].count >= N): return
    if(cats[cat].count < N):
       cats[cat].count += 1
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
   f.write(gen + " " + "F " + str(cats[key].actFem) + " " + str(cats[key].passFem))
   if(cats[key].actFem != 0): f.write(" " + str(cats[key].passFem/float(cats[key].actFem)) + "\n")
   f.write(gen + " " + "M " + str(cats[key].actMal) + " " + str(cats[key].passMal))
   if(cats[key].actMal != 0): f.write(" " + str(cats[key].passMal/float(cats[key].actMal)) + "\n")
f.close
