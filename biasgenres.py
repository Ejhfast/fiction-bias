import math
from collections import defaultdict
import cPickle as pickle
import numpy
import graph

MINPMI = -50
BINNUM = 50

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

def calcAveGivenGrouping(num, f, row, col):
   cats = {}
   diffs = {}
   f = open(f, "r")
   
   def avepmi(cat, pmih, pmis):
      for k,v in pmih.iteritems():
         if((pmis[k] != 0) and (pmih[k] != 0) and pmis[k] > MINPMI and pmis[k] > MINPMI):
            diffs[cat].append(abs((pmis[k] - pmih[k])))
     
   for x in range (0, num):
      cats[x] = Cat()
      diffs[x] = []
      cat = pickle.load(f)
      cats[cat].pmi_h = pickle.load(f)
      cats[cat].pmi_s = pickle.load(f)
      cats[cat].pmi_her = pickle.load(f)
      cats[cat].pmi_him = pickle.load(f)
      cats[cat].pmi_her_pos = pickle.load(f)
      cats[cat].pmi_his = pickle.load(f)
      cats[cat].pmi_sobj = pickle.load(f)
      cats[cat].pmi_hobj = pickle.load(f)
      avepmi(x, cats[x].pmi_h, cats[x].pmi_s)
      avepmi(x, cats[x].pmi_his, cats[x].pmi_her)
      avepmi(x, cats[x].pmi_hobj, cats[x].pmi_sobj)
      avepmi(x, cats[x].pmi_his, cats[x].pmi_her_pos)
      if len(diffs[x]) != 0:
         ave = numpy.mean(diffs[x])
         std = numpy.std(diffs[x])
      else:
         ave = 0
         std = 0
      print("Average for", x, "is: ", ave, "Std dev is: ", std)
      
   
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
   
   graph.multhisto(row, col, num, diffs, BINNUM)     
   queryForVerbFreq()
   queryForNounFreq()
   f.close()

f1 = "cat00000.pmis.txt"
f2 = "rat00000.pmis.txt"
calcAveGivenGrouping(5, f2, 2, 3)
calcAveGivenGrouping(25, f1, 6, 4)