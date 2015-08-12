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

MAXBUFF = 50
MAXBUFFA = 3
CONVOBUFFLENGTH = 150
CONVOBUFF2LENGTH = 30

dial = []
dial2 = []
adj = []

def addtoquote(tk):
   if(tk == "\""):
      return ""
   elif((tk in string.punctuation) or tk.count("\'") != 0):
      return tk
   else:
      return " " + tk

def extractDialogBack(buff, gender, quotes):
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
                 extractDialogBack(buff, gender, quotes)
                 convoBuff = 0
              if (buff[len(buff) - 1] == "he" or names.ismalename(buff[len(buff) - 1])):
                 gender = "male" 
                 extractDialogBack(buff, gender, quotes)
                 convoBuff = 0
              
           if(names.isfemalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "female"
                 extractDialogBack(buff, gender, quotes)
                 convoBuff = 0
           if(names.ismalename(tk.lower_)):
              if (speakerverb(bufftk[len(bufftk) - 1])):
                 gender = "male"
                 extractDialogBack(buff, gender, quotes)
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
             if (buffA[len(buffA) - 1].lower_ == "her"):
                adj.append([tk.lower_, "female"])
             if (buffA[len(buffA) - 1].lower_ == "his"):
                adj.append([tk.lower_, "male"])
             
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
  except UnicodeDecodeError:
      pass
      
for line in fileinput.input():
  analyze(line)
