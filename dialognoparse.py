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
from collections import deque


nlp = spacy.en.English()

stories = {}
f = open("/home/ubuntu/ebs/dataset/story_chapters/part-m-00000", "r")
for line in f:
  storyID, textID = [x.rstrip() for x in line.split("\t")]
  stories[textID] = storyID
f.close

categories = {}
writers = {}
ratings = {}

N = 200000
MAXBUFF = 50

f = open("/home/ubuntu/ebs/dataset/story_details/part-m-00000", "r")
for line in f:
  writerID, storyID, categoryID, rating = [x.rstrip() for x in line.split("\t")]
  categories[storyID] = categoryID
  writers[storyID] = writerID
  ratings[storyID] = rating
f.close

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

nameList = defaultdict(Set)

fdial = open("gendereddialogsmall.txt", 'w')

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif(tk in string.punctuation):
      return tk
   else:
      return " " + tk

def checkUniq(tk, cat, storyid):
  if (names.isfemalename(tk) or names.ismalename(tk)):
     if(tk not in nameList[storyid]): 
        nameList[storyid].add(tk)
        if(names.isfemalename(tk)):
           cats[cat].femUniq += 1
        elif(names.ismalename(tk)):
           cats[cat].malUniq += 1

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif((tk in string.punctuation) or tk.count("\'") != 0):
      return tk
   else:
      return " " + tk

def extractDialogBack(buff, gender, cat, storyid):
  #print(buff[len(buff) - 2])
  #
  if(buff.count("\"") >= 2 and buff[len(buff) - 2] == "\""):
     buff.reverse()
     quote = ""
     for i in range (buff.index("\"") + 1, len(buff)):
        if(buff[i].count("\"") != 0): break
        quote = addtoquote(buff[i]) + quote
     fdial.write(quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
     buff.reverse()
     return True
  return False
                   
def countVerbs(chapter, cat, storyid):
  buff = []
  bufftk = []
  inquote = False
  gend = ""
  quote = ""
  count = 0
#  for sen in chapter.split("." or "!" or "?"):
#    if(cats[cat].count >= N): return
#    if(cats[cat].count < N):
#       cats[cat].count += 1
  try:
     for tk in nlp(unicode(chapter), parse=False): 
        if(len(buff) >= 2):
           if(inquote == True):
             if(tk.lower_== ("\"") or count >= 30):
               fdial.write(quote + "\t" + gend + "\t" + str(cat) + "\t" + str(storyid) + "\n")
               inquote = False
               gend = ""
               quote = ""
               count = 0
             else:
               count += 1
               quote += addtoquote(tk.lower_)
             continue
                
           if(speakerverb(tk.lemma_)):
              if (buff[len(buff) - 1] == "she" or names.isfemalename(buff[len(buff) - 1])):
                 if(tk.lemma == "state"): print buff[len(buff) - 1]
                 gender = "female"
                 cats[cat].femDialog += 1
                 extractDialogBack(buff, gender, cat, storyid)
              if (buff[len(buff) - 1] == "he" or names.ismalename(buff[len(buff) - 1])):
                 gender = "male"
                 cats[cat].malDialog += 1   
                 extractDialogBack(buff, gender, cat, storyid)
              checkUniq(buff[len(buff) - 1], cat, storyid)
              
           if(names.isfemalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "female"
                 cats[cat].femDialog += 1
                 checkUniq(tk.lower_, cat, storyid)
                 extractDialogBack(buff, gender, cat, storyid)
           if(names.ismalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "male"
                 cats[cat].malDialog += 1
                 checkUniq(tk.lower_, cat, storyid)
                 extractDialogBack(buff, gender, cat, storyid)
                 
           if(tk.lower_ == ("\"")):
             if(speakerverb(bufftk[len(bufftk) - 1])):
                if (buff[len(buff) - 2] == "she" or names.isfemalename(buff[len(buff) - 2])):
                   gend = "female"
#                   cats[cat].femDialog += 1
                   inquote = True
                if (buff[len(buff) - 2] == "he" or names.ismalename(buff[len(buff) - 2])):
                   gend = "male"
#                   cats[cat].malDialog += 1   
                   inquote = True
#                checkUniq(buff[len(buff) - 2])
              
        if(len(buff) >= MAXBUFF):
           bufftk.remove(bufftk[0])
           buff.remove(buff[0])
        buff.append(tk.lower_)
        bufftk.append(tk.lemma_)
  except UnicodeDecodeError:
      pass
           
for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countVerbs(chapter, cat, storyid)
  
f = open("dialogtiny.txt", 'w')
genre = graph.getGenres()
for key in sorted(cats):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + " " + str(cats[key].femDialog) + " " + str(cats[key].malDialog))
   if(cats[key].malDialog != 0): f.write(" Ratio:" + str(cats[key].femDialog/float(cats[key].malDialog)))
   f.write(" " + str(cats[key].femUniq) + " " + str(cats[key].malUniq))
   if(cats[key].malUniq != 0): f.write(" Ratio:" + str(cats[key].femUniq/float(cats[key].malUniq)))
   f.write("\n")
f.close