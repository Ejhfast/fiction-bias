import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle
from sets import Set
import names

N = 100000
CONVOLENGTH = 5
BUFFERLENGTH = 3

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

class Cat:
  def __init__(self):
     self.storyBechFreq = defaultdict(int)
     self.failed = []
     self.passed = []

cats = {}
for x in range (0, 25):
  cats[x] = Cat()

counts = defaultdict(int)

nlp = spacy.en.English()
 
def speakerverb(word):
   if(word == 'say' or word == 'answer' or word == 'reply' or word == 'shout' or word == 'whisper' or word == 'yell'
    or word == 'whine' or word == 'stammer' or word == 'respond' or word == 'remind' or word == 'remark' or word == 'utter'
    or word == 'recall' or word == 'ask' or word == 'hint' or word == 'groan' or word == 'claim' or word == 'declare' or word == 'describe'
    or word == 'interject' or word == 'mutter' or word == 'mumble' or word == 'continue' or word == 'clarify'):
       return True
   else:
       return False 

       
def bechdel(chapter, cat):
  first = True
  start = False
  countConvo = 0
  countBuffer = 0
  name = ""
  for sen in chapter.split("." or "!" or "?"):
    if (countConvo > CONVOLENGTH):
       return True
    if (countBuffer > BUFFERLENGTH):
       countBuffer = 0
       first = True
       name = ""
    if(counts[cat] >= N):
       return
    else:
       counts[cat] += 1
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      dialog = False
      for tk in tokens:
        if(tk.lower_ == "\""): dialog = True
        if ((tk.lower_ == 'he' or names.ismalename(tk.lower_)) and dialog == True):
           break
           first = True
           start = False
           countConvo = 0
           countBuffer = 0
           name = ""
        if(start == False and tk.pos_ == "VERB" and speakerverb(tk.lemma_)):
           for x in tk.children:
              if(names.isfemalename(x.lower_) and first == True):
                 name = x.lower_
                 first = False
              elif (x.lower_ != name and names.isfemalename(x.lower_)):
                 start = True
      if (first == False):
         countBuffer += 1
      if (start == True and dialog == True):
         countConvo += 1
         
    except UnicodeDecodeError:
      pass
  return False
                    

#if this works, next step is to find genres for ones that pass

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  if(bechdel(chapter, cat)):
     cats[cat].storyBechFreq[storyid] += 1
     cats[cat].passed.append(storyid)
  else:
     print(cat)
     cats[cat].failed.append(storyid)

f = open("bechdeltesetscateg.txt", 'w')

for cat in range (0, 25):
   for key in sorted(cats[cat].storyBechFreq):
      f.write("Genre: " + str(cat) + "\n")
      f.write(key + "," + str(cats[cat].storyBechFreq[key]) + "\n")
   f.write("Num pass bechtel:" + str(len(cats[cat].passed)) + " Num fail bechtel:" + str(len(cats[cat].failed)) + "\n")
