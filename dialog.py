import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle
from passactdata import verbs
import names
import graph
from speakerverbs import speakerverb

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
     self.femDialog = 0
     self.malDialog = 0

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
            
        if(tk.pos_ == "VERB" and speakerverb(tk.lemma)):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "she" or names.isfemalename(x.lower_)):
                   cats[cat].femDialog += 1
                elif (x.lower_ == "he" or names.ismalename(x.lower_)):
                   cats[cat].malDialog += 1
    except UnicodeDecodeError:
      pass

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countVerbs(chapter, cat)
  
f = open("dialogtiny.txt", 'w')
genre = graph.getGenres()
for key in sorted(cats):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + ", " + "Female dialogue: " + str(cats[key].femDialog) + ", " + "Male dialogue: " + str(cats[key].malDialog) + "\n")
   if(cats[key].malDialog != 0): f.write("Ratio:" + str(cats[key].femDialog/float(cats[key].malDialog)) + "\n")
   f.write("\n") 
f.close

