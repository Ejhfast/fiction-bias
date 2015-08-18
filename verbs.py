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
MAXBUFF = 3

f = open("/home/ubuntu/ebs/dataset/story_details/part-m-00000", "r")
for line in f:
  writerID, storyID, categoryID, rating = [x.rstrip() for x in line.split("\t")]
  categories[storyID] = categoryID
  writers[storyID] = writerID
  ratings[storyID] = rating
f.close

f = open("verbs.txt", 'w')

def countVerbs(chapter, cat, storyid):
#  for sen in chapter.split("." or "!" or "?"):
#    if(cats[cat].count >= N): return
#    if(cats[cat].count < N):
#       cats[cat].count += 1
  buff = []
  try:
     for tk in nlp(unicode(chapter), parse=False):
        if(len(buff) >= 2):
           if(tk.pos_ == 'VERB'):
             if (buff[len(buff) - 1].lower_ == "she" or names.isfemalename(buff[len(buff) - 1].lower_) or genderedterms.isfemaleterm(buff[len(buff) - 1].lower_)):
                f.write(storyid + "\t" + str(cat) + "\t" + tk.lemma_ + "\t" + "female" + "\n")
             if (buff[len(buff) - 1].lower_ == "he" or names.ismalename(buff[len(buff) - 1].lower_) or genderedterms.ismaleterm(buff[len(buff) - 1].lower_)):
                f.write(storyid + "\t" + str(cat) + "\t" + tk.lemma_ + "\t" + "male" + "\n")
             
             if (buff[len(buff) - 1].pos_ == "VERB"):
                if (buff[len(buff) - 2].lower_ == "she" or names.isfemalename(buff[len(buff) - 2].lower_) or genderedterms.isfemaleterm(buff[len(buff) - 2].lemma_)):
                  f.write(storyid + "\t" + str(cat) + "\t" + buff[len(buff) - 1].lemma_ + " " + tk.lemma_ + "\t" + "female" + "\n")
                if (buff[len(buff) - 2].lower_ == "he" or names.ismalename(buff[len(buff) - 2].lower_) or genderedterms.ismaleterm(buff[len(buff) - 2].lemma_)):
                  f.write(storyid + "\t" + str(cat) + "\t" + buff[len(buff) - 1].lemma_ + " " + tk.lemma_ + "\t" + "male" + "\n")
                
        if(len(buff) >= MAXBUFF):
           buff.remove(buff[0])
        if(tk.pos_ != 'ADV' and tk.lower_ != 'to'):
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
