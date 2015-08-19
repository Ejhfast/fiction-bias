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

liwc_cache = cPickle.load(open("liwc_cache.pkl","rb"))

MAXBUFF = 50
MAXBUFFA = 3
CONVOBUFFLENGTH = 150
CONVOBUFF2LENGTH = 30

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif((tk in string.punctuation) or tk.count("\'") != 0):
      return tk
   else:
      return " " + tk

def extractDialogBack(buff, gender, quotes, dial, dial2):
  #print(buff[len(buff) - 2])
  #
  if(buff.count("\"") >= 2 and buff[len(buff) - 2] == "\""):
     buff.reverse()
     quote = ""
     for i in range (buff.index("\"") + 1, len(buff)):
        if(buff[i].count("\"") != 0): break
        quote = addtoquote(buff[i]) + quote
     dial.append([quote, gender])
     if(len(quotes) == 1):
        dial2.append(quotes[0] + quote + "\t" + gender)
        quotes.remove(quotes[0])
     else:
        quotes.append(quote + "\t" + gender + "\t")
     buff.reverse()
  return False

def analyze(chapter):
  dial = []
  dial2 = []
  adj = []
  verb = []
  buff = []
  bufftk = []
  buffA = []
  buffV = []
  inquote = False
  gend = ""
  quote = ""
  count = 0
  convoBuff = CONVOBUFFLENGTH
  inConvo = False
  convoBuff2 = CONVOBUFF2LENGTH
  quotes = []
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
                  dial2.append(quotes[0] + quote + "\t" + gend)
                  quotes.remove(quotes[0])
               else:
                  quotes.append(quote + "\t" + gend + "\t")
               dial.append([quote, gend])
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
                 extractDialogBack(buff, gender, quotes, dial, dial2)
                 convoBuff = 0
              if (buff[len(buff) - 1] == "he" or names.ismalename(buff[len(buff) - 1])):
                 gender = "male"
                 extractDialogBack(buff, gender, quotes, dial, dial2)
                 convoBuff = 0

           if(names.isfemalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "female"
                 extractDialogBack(buff, gender, quotes, dial, dial2)
                 convoBuff = 0
           if(names.ismalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "male"
                 extractDialogBack(buff, gender, quotes, dial, dial2)
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

        #Adjective extraction#
        if(len(buffA) >= 2):
           if(tk.pos_ == 'ADJ'):
            #  if (buffA[len(buffA) - 1].lower_ == "her"):
            #     adj.append([tk.lower_, "female"])
            #  if (buffA[len(buffA) - 1].lower_ == "his"):
            #     adj.append([tk.lower_, "male"])

             if (buffA[len(buffA) - 1].lemma_ == "be"):
                if (buffA[len(buffA) - 2].lower_ == "she" or names.isfemalename(buffA[len(buffA) - 2].lower_) or genderedterms.isfemaleterm(buffA[len(buffA) - 2].lemma_)):
                  adj.append([tk.lower_, "female"])
                if (buffA[len(buffA) - 2].lower_ == "he" or names.ismalename(buffA[len(buffA) - 2].lower_) or genderedterms.ismaleterm(buffA[len(buffA) - 2].lemma_)):
                  adj.append([tk.lower_, "male"])

           if(genderedterms.isfemaleterm(tk.lemma_)):
              if (buffA[len(buffA) - 1].pos_ == 'ADJ'):
                adj.append([buffA[len(buffA) - 1].lower_, "female"])
           elif(genderedterms.ismaleterm(tk.lemma_)):
              if (buffA[len(buffA) - 1].pos_ == 'ADJ'):
                adj.append([buffA[len(buffA) - 1].lower_, "male"])

        if(len(buffA) >= MAXBUFFA):
           buffA.remove(buffA[0])
        if(tk.pos_ != 'ADV'):
           buffA.append(tk)
           
        #verb extraction#   
        if(len(buffV) >= 2):
           if(tk.pos_ == 'VERB'):
             if (buffV[len(buffV) - 1].lower_ == "she" or names.isfemalename(buffV[len(buffV) - 1].lower_) or genderedterms.isfemaleterm(buffV[len(buffV) - 1].lower_)):
                verb.append([tk.lemma_, "female"])
             if (buffV[len(buffV) - 1].lower_ == "he" or names.ismalename(buffV[len(buffV) - 1].lower_) or genderedterms.ismaleterm(buffV[len(buffV) - 1].lower_)):
                verb.append([tk.lemma_, "male"])
             
             if (buffV[len(buffV) - 1].pos_ == "VERB"):
                if (buffV[len(buffV) - 2].lower_ == "she" or names.isfemalename(buffV[len(buffV) - 2].lower_) or genderedterms.isfemaleterm(buffV[len(buffV) - 2].lemma_)):
                  verb.append([buffV[len(buffV) - 1].lemma_ + " " + tk.lemma_, "female"])
                if (buffV[len(buffV) - 2].lower_ == "he" or names.ismalename(buffV[len(buffV) - 2].lower_) or genderedterms.ismaleterm(buffV[len(buffV) - 2].lemma_)):
                  verb.append([buffV[len(buffV) - 1].lemma_ + " " + tk.lemma_, "male"])
                
        if(len(buffV) >= MAXbuffV):
           buffV.remove(buffV[0])
        if(tk.pos_ != 'ADV' and tk.lower_ != 'to'):
           buffV.append(tk)
  except UnicodeDecodeError:
      pass
  print(str(verb))
  return {"dialog":dial,"dialog-pairs":dial2,"adj":adj,"verb":verb}

def over_liwc(w):
  if w in liwc_cache:
    for k,v in liwc_cache[w].iteritems():
        yield k,v

def lookup_liwc(dias, lookup=over_liwc):
  count_cats = defaultdict(lambda: defaultdict(float))
  for d in dias:
    words = [x.lower().rstrip() for x in d[0].split(" ") if len(x.rstrip())>0]
    for w in words:
      for k,v in lookup(w):
        count_cats[d[1]][k] += v
  count_cats["male"]["total_number"] = len([x for x in dias if x[1] == "male"])
  count_cats["female"]["total_number"] = len([x for x in dias if x[1] == "female"])
  return count_cats

def gender_count(adjs):
  def over_adj(w): yield w,1
  count_adjs = lookup_liwc(adjs, over_adj)
  a4temp = []
  for a in set(count_adjs["male"].keys()+count_adjs["female"].keys()):
    direction, odds = None, None
    male_ = round(count_adjs["male"][a] / count_adjs["male"]["total_number"],3)
    female_ = round(count_adjs["female"][a] / count_adjs["female"]["total_number"],3)
    if male_ > female_:
      direction = "male"
      if female_ > 0:
        odds = round(male_/female_,2)
      else: odds = "inf"
    else:
      direction = "female"
      if male_ > 0:
        odds = round(female_/male_,2)
      else: odds = "inf"
    a4temp.append({"name":a, "male":male_,
                     "female":female_, "direction":direction, "odds":odds})
    a4temp = sorted(a4temp,key=lambda x: x["male"]+x["female"],reverse=True)
  return a4temp

def dialog_count(dias):
  lookat=["Home","Family","Sexual","Anger","Sad","Posemo","Negemo","Money","Friends"]
  count_cats = lookup_liwc(dias)
  d4temp = []
  for t in lookat:
    direction, odds = None, None
    male_ = round(count_cats["male"][t] / count_cats["male"]["total_number"],3)
    female_ = round(count_cats["female"][t] / count_cats["female"]["total_number"],3)
    if male_ > female_:
      direction = "male"
      if female_ > 0:
        odds = round(male_/female_,2)
      else: odds = "inf"
    else:
      direction = "female"
      if male_ > 0:
        odds = round(female_/male_,2)
      else: odds = "inf"
    d4temp.append({"name":t, "male":male_,
                         "female":female_, "direction":direction, "odds":odds})
    d4temp = sorted(d4temp,key=lambda x: x["male"]+x["female"],reverse=True)
  return d4temp

def compute_stereotype(lsts):
  liwc_cats = []
  for l in lsts:
    liwc_cats.append(lookup_liwc(l))
  domestic = ["Home","Money","Family","Social"]
  social = ["Friends"]
  agressive = ["Anger","Swear"]
  sexual = ["Sexual"]
  independent = ["Achieve"]
  # want independent/dependent, appearance terms
  men = agressive + sexual + independent
  women = domestic + social
  num,denom = 0,0
  for c in men:
    for cat in liwc_cats:
      num += cat["male"][c] / cat["male"]["total_number"]
      denom += cat["female"][c] / cat["female"]["total_number"]
  for c in women:
    for cat in liwc_cats:
      num += cat["female"][c] / cat["female"]["total_number"]
      denom += cat["male"][c] / cat["male"]["total_number"]
  if(num == 0 and denom == 0): return 0
  elif(num > 0 and denom == 0): return "inf"
  return round(float(num)/float(denom),3)

def main():
    for line in fileinput.input():
        cid,txt = [x.rstrip() for x in txt.split("\t")]
        dicts = analyze(txt)
        score = compute_stereotype([dicts["adj"],dicts["dialog"]])
        print("\t".join([cid,str(score)]))

if __name__ == "__main__":
    main()
