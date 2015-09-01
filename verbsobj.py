import fileinput
from collections import defaultdict
import spacy.en
import names
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
MAXBUFF = 5

f = open("/home/ubuntu/ebs/dataset/story_details/part-m-00000", "r")
for line in f:
  writerID, storyID, categoryID, rating = [x.rstrip() for x in line.split("\t")]
  categories[storyID] = categoryID
  writers[storyID] = writerID
  ratings[storyID] = rating
f.close

f = open("verbsobj.txt", 'w')

def gender(pron):
  if(pron == 'her'):
    return 'female'
  elif(pron == 'him'):
    return 'male'
  else:
    return 'error'

def checkPronouns(cat, storyid, orgpron, checkpron, verb, other):
  if (checkpron == 'she' or names.isfemalename(checkpron) or genderedterms.isfemaleterm(checkpron)):
    f.write(storyid + "\t" + str(cat) + "\t" + verb + other + "\t" + "female " + gender(orgpron) + "\n")
  if (checkpron == 'he' or names.ismalename(checkpron) or genderedterms.ismaleterm(checkpron)):
    f.write(storyid + "\t" + str(cat) + "\t" + verb + other + "\t" + "male " + gender(orgpron) + "\n")
    
def countVerbs(chapter, cat, storyid):
#  for sen in chapter.split("." or "!" or "?"):
#    if(cats[cat].count >= N): return
#    if(cats[cat].count < N):
#       cats[cat].count += 1
  buff = []
  try:
     for tk in nlp(unicode(chapter), parse=False):
        if(len(buff) >= 2):
           if(tk.pos_ != 'NOUN'):
             first = buff[len(buff) - 1]
             second = buff[len(buff) - 2]
             third = buff[len(buff) - 3]
             fourth =  buff[len(buff) - 4]
             if((first.lower_ == 'him' or first.lower_ == 'her') and (second.pos_ == 'VERB')):
               checkPronouns(cat, storyid, first.lower_, third.lower_, second.lemma_, "")
             if((first.lower_ == 'him' or first.lower_ == 'her') and (third.pos_ == 'VERB')):
               checkPronouns(cat, storyid, first.lower_, fourth.lower_, third.lemma_, " " + second.lower_)
                
        if(len(buff) >= MAXBUFF):
           buff.remove(buff[0])
        if(tk.pos_ != 'ADV'):
           buff.append(tk)
  except UnicodeDecodeError:
      pass

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  print(id_)
  storyid = stories[id_]
  rating = int(ratings[storyid])
  cat = int(categories[storyid])
  countVerbs(chapter, cat, storyid)

