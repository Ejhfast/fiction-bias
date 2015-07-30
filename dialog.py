import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle
from passactdata import verbs
import names
import graph
from speakerverbs import speakerverb
from sets import Set
import string

stories = {}
f = open("/home/ubuntu/ebs/dataset/story_chapters/part-m-00000", "r")
for line in f:
  storyID, textID = [x.rstrip() for x in line.split("\t")]
  stories[textID] = storyID
f.close

categories = {}
writers = {}
ratings = {}

N = 100000

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
     self.femUniq = 0
     self.malUniq = 0
     self.count = 0

cats = {}
for x in range (0, 25):
  cats[x] = Cat()

nameList = Set([])

fdial = open("gendereddialog.txt", 'w')

def extractDialog(sen, gender, cat, storyid, chapter):
   print(sen)
   print(chapter)
   before, speaking, after = [x.rstrip() for x in line.split("\"")]
   fdial.write(speaking + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid))

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif(tk in string.punctuation):
      return tk
   else:
      return " " + tk

def countVerbs(chapter, cat, storyid):
  gender = ""
  inquote = False
  quote = ""
  for sen in chapter.split("." or "!" or "?"):
    if(cats[cat].count >= N): return
    if(cats[cat].count < N):
       cats[cat].count += 1
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens: 
        if(tk.pos_ == "VERB" and speakerverb(tk.lemma_)):
           for x in tk.lefts:
             if (x.lower_ == "she" or names.isfemalename(x.lower_)):
                gender = "female"
                cats[cat].femDialog += 1
                #extractDialog(sen, "female", cat, storyid, chapter)
             if (x.lower_ == "he" or names.ismalename(x.lower_)):
                gender = "male"
                cats[cat].malDialog += 1   
                #extractDialog(sen, "male", cat, storyid)
             if (names.isfemalename(x.lower_) or names.ismalename(x.lower_)):
                if(x.lower_ not in nameList): 
                   nameList.add(x.lower_)
                   if(names.isfemalename(x.lower_)):
                      cats[cat].femUniq += 1
                   elif(names.ismalename(x.lower_)):
                      cats[cat].malUniq += 1
             
        if(inquote == True): quote += addtoquote(tk.lower_)
        if(tk.lower_.count("\"") == 1):
           if(inquote == False):
              quote = ""
              inquote = True
           else:
              inquote = False
              if(gender != ""):
                fdial.write(quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
              gender = ""
              

      if(inquote == False):
        if(gender != ""):
          fdial.write(quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
        gender = ""
        quote = ""
             
    except UnicodeDecodeError:
      pass

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countVerbs(chapter, cat, storyid)
  
f = open("dialogtest.txt", 'w')
genre = graph.getGenres()
for key in sorted(cats):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + " " + "Female dialogue: " + str(cats[key].femDialog) + ", " + "Male dialogue: " + str(cats[key].malDialog) + "\n")
   if(cats[key].malDialog != 0): f.write("Ratio:" + str(cats[key].femDialog/float(cats[key].malDialog)) + "\n")
   f.write(gen + ", " + "Female unique: " + str(cats[key].femUniq) + ", " + "Male unique: " + str(cats[key].malUniq) + "\n")
   if(cats[key].malUniq != 0): f.write("Ratio:" + str(cats[key].femUniq/float(cats[key].malUniq)) + "\n")
   f.write("\n") 
f.close

