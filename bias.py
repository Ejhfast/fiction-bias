import math
from collections import defaultdict
import cPickle as pickle
import numpy

f = open("pmis.txt", "r")

pmi_h = pickle.load(f)
pmi_s = pickle.load(f)
pmi_her = pickle.load(f)
pmi_him = pickle.load(f)
pmi_her_pos = pickle.load(f)
pmi_his = pickle.load(f)
pmi_sobj = pickle.load(f)
pmi_hobj = pickle.load(f)
#tot_h = pickle.load(f)
#tot_s = pickle.load(f)
#tot_her = pickle.load(f)
#tot_him = pickle.load(f)
#tot_her_pos = pickle.load(f)
#tot_his = pickle.load(f)

MINPMI = 0.0
LARGEDIFF = 1.0
#nlp = spacy.en.English()
#
#def calcPMI(pron, word, tot):
#  if(tot == 0): return 0
#  wordGivenPron = 1/tot
#  pronGivenWord = (2**(nlp.vocab[pron].prob) * wordGivenPron) /2**(nlp.vocab[unicode(word)].prob)
#  x = pronGivenWord/2**(nlp.vocab[pron].prob)
#  pmi = math.log(x)
#  print(pmi)
#  return pmi
#
#def calcPMIsAndFindMax(prons, freqs, tots, pmis, pronh, freqh, toth, pmih):
#  mxnum = 0.0
#  mx = ""
#  largeAndPos = []
#  for k,v in freqs.iteritems():
#     pmis[k] = calcPMI(prons, k, freqs, tots)
#     pmih[k] = calcPMI(pronh, k, freqh, toth)
#     if(abs(pmis[k] - pmih[k]) >= LARGEANDPOS and (pmis != 0.0 and pmih != 0.0)):
#        largeAndPos.append(k)
##     if(abs(pmis[k] - pmih[k]) > mxnum):
##        mxnum = abs(pmis[k] - pmih[k])
##        mx = k
#  for k,v in freqh.iteritems():
#     if(pmih[k] == 0):
#        pmih[k] = calcPMI(pronh, k, freqh, toth)
#        if(abs(pmis[k] - pmih[k]) >= LARGEANDPOS and (pmis != 0.0 and pmih != 0.0)):
#           largeAndPos.append(k)
##        if(abs(pmis[k] - pmih[k]) > mxnum):
##           mxnum = abs(pmis[k] - pmih[k])
##           mx = k
#  for word in largeAndPos:
#     print (word)
#     print ("Frequency for ", prons, pmis[word], "Frequency for ", pronh, pmih[word])  
##  print ("Max for ", prons, pronh, "is", mx)
##  print ("Frequency for ", prons, pmis[mx], "Frequency for ", pronh, pmih[mx])
#
#calcPMIsAndFindMax(u'she', freq_s, tot_s, pmi_s, u'he', freq_h, tot_h, pmi_h)
#calcPMIsAndFindMax(u'her', freq_her, tot_her, pmi_her, u'him', freq_him, tot_him, pmi_him) 
#calcPMIsAndFindMax(u'her', freq_her_pos, tot_her_pos, pmi_her_pos, u'his', freq_his, tot_his, pmi_his) 
#calcPMIsAndFindMax(u'she', freq_sobj, tot_s, pmi_sobj, u'he', freq_hobj, tot_h, pmi_hobj)  

diffs = []
def findLargeAndPos(pmis, pmih, prons, pronh):
   print("DIFFERENCES BETWEEN", prons, "AND", pronh)
   for k,v in pmis.iteritems():
#      if(pmih[k] == 0):
#         pmih[k] = calcPMI(pronh, k, toth)
      if((pmis[k] != 0) and (pmih[k] != 0)):
         diffs.append(abs(pmis[k] - pmih[k]))
      if(((pmis[k] != 0) and (pmih[k] != 0)) and (abs((pmis[k] - pmih[k])) > LARGEDIFF)):
         print (k)
         print ("Frequency for ", prons, pmis[k], "Frequency for ", pronh, pmih[k])
         print("")
#   for k,v in pmih.iteritems():
#      if(pmis[k] == 0):
##         pmis[k] = calcPMI(prons, k, toth)
#         if(((pmis[k] > MINPMI) or (pmih[k] > MINPMI)) and (abs((pmis[k] - pmih[k])) > LARGEDIFF)):
#            print (k)
#            print ("Frequency for ", prons, pmis[k], "Frequency for ", pronh, pmih[k])
#            print("")


def queryForVerbFreq(pmi_s, pmi_h, pmi_her, pmi_him):
   verb = ""      
   while True:
     verb = input("Enter a verb (Quit to quit, remember the quotation marks!): ")
     if(verb == "Quit"): return
     print ("Frequency for she: ", pmi_s[verb], "Frequency for he: ", pmi_h[verb])
     print ("Frequency for her: ", pmi_her[verb], "Frequency for him: ", pmi_him[verb])
     
def queryForNounFreq(pmi_sobj, pmi_hobj, pmi_her_pos, pmi_his):
   noun = ""
   while True:
      noun = input("Enter a noun (Quit to quit, remember the quotation marks!): ")
      if(noun == "Quit"): return
      print ("Frequency for she: ", pmi_sobj[noun], "Frequency for he: ", pmi_hobj[noun])
      print ("Frequency for her: ", pmi_her_pos[noun], "Frequency for his: ", pmi_his[noun])

findLargeAndPos(pmi_s, pmi_h, u'she', u'he')
findLargeAndPos(pmi_her, pmi_him, u'her', u'him')
findLargeAndPos(pmi_sobj, pmi_hobj, u'she', u'he')
findLargeAndPos(pmi_her_pos, pmi_his, u'her', u'his')
stddev = numpy.std(diffs)
print("Std dev is: ", stddev)      
queryForVerbFreq(pmi_s, pmi_h, pmi_her, pmi_him)
queryForNounFreq(pmi_sobj, pmi_hobj, pmi_her_pos, pmi_his)