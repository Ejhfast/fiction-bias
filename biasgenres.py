import math
from collections import defaultdict
import cPickle as pickle
import spacy.en
import numpy

f = open("cat00000.pmis.txt", "r")

class Cat:
  def __init__(self):
     self.pmi_h = defaultdict(float)
     self.pmi_s = defaultdict(float)
     self.pmi_her = defaultdict(float)
     self.pmi_him = defaultdict(float)
     self.pmi_her_pos = defaultdict(float)
     self.pmi_his = defaultdict(float)
     self.pmi_sobj = defaultdict(float)
     self.pmi_hobj = defaultdict(float)

cats = {}
diffs = {}
for x in range (0, 25):
  cats[x] = Cat()
  diffs[x] = []
  
for x in range (0, 25):
   cat = pickle.load(f)
   cats[cat].pmi_h = pickle.load(f)
   cats[cat].pmi_s = pickle.load(f)
   cats[cat].pmi_her = pickle.load(f)
   cats[cat].pmi_him = pickle.load(f)
   cats[cat].pmi_her_pos = pickle.load(f)
   cats[cat].pmi_his = pickle.load(f)
   cats[cat].pmi_sobj = pickle.load(f)
   cats[cat].pmi_hobj = pickle.load(f)
   
def avepmi(cat, pmih, pmis, pronh, prons):
   count = 0.0
   numer = 0.0
   for k,v in pmih.iteritems():
      if((pmis[k] != 0) and (pmih[k] != 0)):
         count += 1
         numer += abs((pmis[k] - pmih[k]))
         diffs[cat].append(abs((pmis[k] - pmih[k])))
   if(count != 0):
      ave = numer/count
      #print("Average for", cat, "between pronouns", pronh, prons, "is:", ave)
      return ave
   return 0      

for x in range (0, 25):
   avehs = avepmi(x, cats[x].pmi_h, cats[x].pmi_s, "he", "she")
   avehh = avepmi(x, cats[x].pmi_his, cats[x].pmi_her, "his", "her")
   avehsobj = avepmi(x, cats[x].pmi_hobj, cats[x].pmi_sobj, "hobj", "sobj")
   avehhpos = avepmi(x, cats[x].pmi_his, cats[x].pmi_her_pos, "his", "her_pos")
   total = (avehs + avehh + avehsobj + avehhpos)/4.0
   if total != 0:
      std = numpy.std(diffs[x])
   else:
      std = 0
   print("Average for", x, "is: ", total, "Std dev is: ", std)

def queryForVerbFreq():
   verb = ""      
   while True:
     verb = input("Enter a verb (Quit to quit, remember the quotation marks!): ")
     if(verb == "Quit"): return
     while True:
        ct = input("Enter a genre(-1 to quit): ")
        if(ct == -1): return
        print ("Frequency for she: ", cats[ct].pmi_s[verb], "Frequency for he: ", cats[ct].pmi_h[verb])
        print ("Frequency for her: ", cats[ct].pmi_her[verb], "Frequency for him: ", cats[ct].pmi_him[verb])
     #queryForGenre(verb, "pmi_s", "pmi_h", "pmi_her", "pmi_him")
     
     
def queryForNounFreq():
   noun = ""
   while True:
      noun = input("Enter a noun (Quit to quit, remember the quotation marks!): ")
      if(noun == "Quit"): return
      while True:
        ct = input("Enter a genre(-1 to quit): ")
        if(ct == -1): return
        print ("Frequency for she: ", cats[ct].pmi_sobj[noun], "Frequency for he: ", cats[ct].pmi_hobj[noun])
        print ("Frequency for her: ", cats[ct].pmi_her_pos[noun], "Frequency for him: ", cats[ct].pmi_his[noun])
      #queryForGenre(noun, "pmi_sobj", "pmi_hobj", "pmi_her_pos", "pmi_his")
     
queryForVerbFreq()
queryForNounFreq()
