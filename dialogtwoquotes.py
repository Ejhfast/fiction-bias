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
CONVOBUFFLENGTH = 30

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
     self.femInit = 0
     self.malInit = 0
     self.count = 0

cats = {}
for x in range (0, 25):
  cats[x] = Cat()

fdial = open("gendereddialog2.txt", 'w')

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif(tk in string.punctuation):
      return tk
   else:
      return " " + tk

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif((tk in string.punctuation) or tk.count("\'") != 0):
      return tk
   else:
      return " " + tk

def extractDialogBack(buff, gender, cat, storyid, quotes):
  if(buff.count("\"") >= 2 and buff[len(buff) - 2] == "\""):
     buff.reverse()
     quote = ""
     for i in range (buff.index("\"") + 1, len(buff)):
        if(buff[i].count("\"") != 0): break
        quote = addtoquote(buff[i]) + quote
     if(len(quotes) == 1):
        fdial.write(quotes[0] + quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
        quotes.remove(quotes[0])
     else:
        quotes.append(quote + "\t" + gender + "\t")
     buff.reverse()
  return False
                   
def countVerbs(chapter, cat, storyid):
  buff = []
  bufftk = []
  inquote = False
  gend = ""
  quote = ""
  count = 0
  convoBuff = CONVOBUFFLENGTH
  quotes = []
  try:
     for tk in nlp(unicode(chapter), parse=False):
        if (convoBuff > CONVOBUFFLENGTH) and len(quotes) > 0:
           quotes.remove(quotes[0])
        if(len(buff) >= 2):
           if(inquote == True):
             if(tk.lower_== ("\"") or count >= 30):
               if(len(quotes) == 1):
                  fdial.write(quotes[0] + quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
                  quotes.remove(quotes[0])
               else:
                  quotes.append(quote + "\t" + gend + "\t")
               inquote = False
               gend = ""
               quote = ""
               count = 0
               convoBuff = 0
             else:
               count += 1
               quote += addtoquote(tk.lower_)
             continue
                
           if(speakerverb(tk.lemma_)):
              if (buff[len(buff) - 1] == "she" or names.isfemalename(buff[len(buff) - 1])):
                 gender = "female"
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 convoBuff = 0
              if (buff[len(buff) - 1] == "he" or names.ismalename(buff[len(buff) - 1])):
                 gender = "male" 
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 convoBuff = 0
              
           if(names.isfemalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "female"
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 convoBuff = 0
           if(names.ismalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "male"
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 convoBuff = 0
                 
           if(tk.lower_ == ("\"")):
             if(speakerverb(bufftk[len(bufftk) - 1])):
                if (buff[len(buff) - 2] == "she" or names.isfemalename(buff[len(buff) - 2])):
                   gend = "female"
                   inquote = True
                if (buff[len(buff) - 2] == "he" or names.ismalename(buff[len(buff) - 2])):
                   gend = "male"  
                   inquote = True
              
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
