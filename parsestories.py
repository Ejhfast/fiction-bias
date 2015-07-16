import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle

N = 100000
CONVOLENGTH = 10

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

storyBechFreq = defaultdict(int)
cats = {}

nlp = spacy.en.English()
 
def speakerverb(word):
   if(word == 'said' or word == 'answer' or word == 'reply' or word == 'shout' or word == 'whisper' or word == 'yell'
    or word == 'whine' or word == 'stammer' or word == 'respond' or word == 'remind' or word == 'remark' or word == 'utter'
    or word == 'recall' or word == 'ask' or word == 'hint' or word == 'groan' or word == 'claim'):
       return True
   else:
       return False 
  
       
def bechdel(chapter, cat):
  first = True
  start = False
  countConvo = 0
  countBuffer = 0
  for sen in chapter.split("." or "!" or "?"):
    if (countConvo > CONVOLENGTH) return True
    if (countBuffer > BUFFERLENGTH):
       countBuffer = 0
       first = True
    if(cats[cat] >= N):
       return
    else:
       cats[cat] += 1
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
        if (tk.lower == 'he' or ismalename(tk.lower_)):
           break
           first = True
           start = False
           countConvo = 0
           countBuffer = 0
        if(start == False and tk.pos_ == "VERB" and speakerverb(tk.lemma_)):
           for x in tk.children:
              if(isfemalename(x.lower_) and first == True):
                 first = False
              else if (isfemalename(x.lower_)):
                 start = True
      if (first = False):
         countBuffer += 1
      if (start == True):
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
     storyBechFreq[storyid] += 1

