import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle

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

cats = {}

nlp = spacy.en.English()
 
def speakerverb(word):
   if(word == 'said' or word == 'answer' or word == 'reply' or word == 'shout' or word == 'whisper' or word == 'yell'
    or word == 'whine' or word == 'stammer' or word == 'respond' or word == 'remind' or word == 'remark' or word == 'utter'
    or word == 'recall' or word == 'ask' or word == 'hint' or word == 'groan' or word == 'claim'):
       return True
   else:
       return False
       
def bechtal(chapter):
  for sen in chapter.split("." or "!" or "?"):
    if(cats[cat] >= N):
       return
    else:
       cats[cat] += 1
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
      
        if(tk.pos_ == "VERB" and speakerverb(tk.lemma_)):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "she"):
                   
                   
        elif(tk.pos_ == "NOUN"):
#           cats[cat].counts[tk.lemma_] += 1
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "her"):
                   if(cats[cat].count < N):
                      cats[cat].tot_her_pos += 1
                      cats[cat].freq_her_pos[tk.lemma_] +=1
                   if(rats[rat].count < N):
                      rats[rat].tot_her_pos += 1
                      rats[rat].freq_her_pos[tk.lemma_] +=1
                elif (x.lower_ == "his"):
                   if(cats[cat].count < N):
                      cats[cat].tot_his += 1
                      cats[cat].freq_his[tk.lemma_] +=1
                   if(rats[rat].count < N):
                      rats[rat].tot_his += 1
                      rats[rat].freq_his[tk.lemma_] +=1
                    
    except UnicodeDecodeError:
      pass


for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  bechtal(chapter)

