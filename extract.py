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
import genderedterms

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
MAXBUFFA = 3
CONVOBUFFLENGTH = 150
CONVOBUFF2LENGTH = 30

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

nameList = defaultdict(Set)
numFemSpeakers = defaultdict(int)
numMalSpeakers = defaultdict(int)
numFemUniq = defaultdict(int)
numMalUniq = defaultdict(int)
numFemInit = defaultdict(int)
numMalInit = defaultdict(int)

fdial = open("gendereddialog1.txt", 'w')
fdial2 = open("gendereddialog21.txt", 'w')
fadj = open("adjectives1.txt", 'w')

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
           numFemUniq[storyid] += 1
        elif(names.ismalename(tk)):
           cats[cat].malUniq += 1
           numMalUniq[storyid] += 1

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif((tk in string.punctuation) or tk.count("\'") != 0):
      return tk
   else:
      return " " + tk

def checkInit(tk, gender, cat, inConvo, storyid):
  if(inConvo == False):
     if(gender == "female"):
        cats[cat].femInit += 1
        numFemInit[storyid] += 1
     elif(gender == "male"):
        cats[cat].malInit += 1
        numFemInit[storyid] += 1

def extractDialogBack(buff, gender, cat, storyid, quotes):
  #print(buff[len(buff) - 2])
  #
  if(buff.count("\"") >= 2 and buff[len(buff) - 2] == "\""):
     buff.reverse()
     quote = ""
     for i in range (buff.index("\"") + 1, len(buff)):
        if(buff[i].count("\"") != 0): break
        quote = addtoquote(buff[i]) + quote
     fdial.write(quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
     if(len(quotes) == 1):
        fdial2.write(quotes[0] + quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
        quotes.remove(quotes[0])
     else:
        quotes.append(quote + "\t" + gender + "\t")
     buff.reverse()
  return False
                   
def countVerbs(chapter, cat, storyid):
  buff = []
  bufftk = []
  buffA = []
  inquote = False
  gend = ""
  quote = ""
  count = 0
  convoBuff = CONVOBUFFLENGTH
  inConvo = False
  convoBuff2 = CONVOBUFF2LENGTH
  quotes = []
#  for sen in chapter.split("." or "!" or "?"):
#    if(cats[cat].count >= N): return
#    if(cats[cat].count < N):
#       cats[cat].count += 1
  try:
     for tk in nlp(unicode(chapter), parse=False):
        #Dialogue extraction#
        convoBuff += 1
        if (convoBuff > CONVOBUFFLENGTH):
           inConvo = False
        else:
           inConvo = True 
        if (convoBuff2 > CONVOBUFF2LENGTH) and len(quotes) > 0:
           quotes.remove(quotes[0])
        if(len(buff) >= 2):
           if(inquote == True):
             if(tk.lower_== ("\"") or count >= 30):
               if(len(quotes) == 1):
                  fdial2.write(quotes[0] + quote + "\t" + gender + "\t" + str(cat) + "\t" + str(storyid) + "\n")
                  quotes.remove(quotes[0])
               else:
                  quotes.append(quote + "\t" + gend + "\t")
               fdial.write(quote + "\t" + gend + "\t" + str(cat) + "\t" + str(storyid) + "\n")
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
                 cats[cat].femDialog += 1
                 numFemSpeakers[storyid] += 1
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 checkInit(buff[len(buff) - 1], gender, cat, inConvo, storyid)
                 convoBuff = 0
              if (buff[len(buff) - 1] == "he" or names.ismalename(buff[len(buff) - 1])):
                 gender = "male"
                 cats[cat].malDialog += 1
                 numMalSpeakers[storyid] += 1   
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 checkInit(buff[len(buff) - 1], gender, cat, inConvo, storyid)
                 convoBuff = 0
              checkUniq(buff[len(buff) - 1], cat, storyid)
              
           if(names.isfemalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "female"
                 cats[cat].femDialog += 1
                 checkUniq(tk.lower_, cat, storyid)
                 numFemSpeakers[storyid] += 1
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 checkInit(tk.lower_, gender, cat, inConvo, storyid)
                 convoBuff = 0
           if(names.ismalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "male"
                 cats[cat].malDialog += 1
                 checkUniq(tk.lower_, cat, storyid)
                 numMalSpeakers[storyid] += 1
                 extractDialogBack(buff, gender, cat, storyid, quotes)
                 checkInit(tk.lower_, gender, cat, inConvo, storyid)
                 convoBuff = 0
                 
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
        
        #Adjective extraction#
        if(len(buffA) >= 2):
           if(tk.pos_ == 'ADJ'):
             if (buffA[len(buffA) - 1].lower_ == "her"):
                fadj.write(storyid + "\t" + str(cat) + "\t" + tk.lower_ + "\t" + "female" + "\n")
             if (buffA[len(buffA) - 1].lower_ == "him"):
                fadj.write(storyid + "\t" + str(cat) + "\t" + tk.lower_ + "\t" + "male" + "\n")
             
             if (buffA[len(buffA) - 1].lemma_ == "be"):
                if (buffA[len(buffA) - 2].lower_ == "she" or names.isfemalename(buffA[len(buffA) - 2].lower_) or genderedterms.isfemaleterm(buffA[len(buffA) - 2].lemma_)):
                  fadj.write(storyid + "\t" + str(cat) + "\t" + tk.lower_ + "\t" + "female" + "\n")
                if (buffA[len(buffA) - 2].lower_ == "he" or names.ismalename(buffA[len(buffA) - 2].lower_) or genderedterms.ismaleterm(buffA[len(buffA) - 2].lemma_)):
                  fadj.write(storyid + "\t" + str(cat) + "\t" + tk.lower_ + "\t" + "male" + "\n")
           
           if(genderedterms.isfemaleterm(tk.lemma_)):
              if (buffA[len(buffA) - 1].pos_ == 'ADJ'):
                fadj.write(storyid + "\t" + str(cat) + "\t" + buffA[len(buffA) - 1].lower_ + "\t" + "female" + "\n")
           elif(genderedterms.ismaleterm(tk.lemma_)):
              if (buffA[len(buffA) - 1].pos_ == 'ADJ'):
                fadj.write(storyid + "\t" + str(cat) + "\t" + buffA[len(buffA) - 1].lower_ + "\t" + "male" + "\n")
                
        if(len(buffA) >= MAXBUFFA):
           buffA.remove(buffA[0])
        if(tk.pos_ != 'ADV'):
           buffA.append(tk)
  except UnicodeDecodeError:
      pass
           
for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countVerbs(chapter, cat, storyid)
  
f = open("dialog1.txt", 'w')
f2 = open("storydialog1.txt", 'w')
genre = graph.getGenres()
for key in sorted(cats):
   gen = ""
   if (key in genre):
      gen = genre[key]
   f.write(gen + " " + str(cats[key].femDialog) + " " + str(cats[key].malDialog))
   if(cats[key].malDialog != 0): f.write(" Ratio:" + str(cats[key].femDialog/float(cats[key].malDialog)))
   f.write(" " + str(cats[key].femUniq) + " " + str(cats[key].malUniq))
   if(cats[key].malUniq != 0): f.write(" Ratio:" + str(cats[key].femUniq/float(cats[key].malUniq)))
   f.write(" " + str(cats[key].femInit) + " " + str(cats[key].malInit))
   if(cats[key].malInit != 0): f.write(" Ratio:" + str(cats[key].femInit/float(cats[key].malInit)))
   f.write("\n")
f.close

for key in sorted(nameList):
   f2.write(key + "\t" + str(numFemSpeakers[key]) + "\t" + str(numMalSpeakers[key]) + "\t" + str(numFemUniq[key]) + "\t" + str(numMalUniq[key]) + "\t" + str(numFemInit[key]) + "\t" + str(numMalInit[key]) + "\n")
