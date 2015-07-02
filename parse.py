import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle

stories = {}
f = open("/home/ubuntu/metadata/chapters/story_chapters/part-m-00000", "r")
for line in f:
  storyID, textID = [x.rstrip() for x in line.split("\t")]
  stories[textID] = storyID
f.close

categories = {}
f = open("/home/ubuntu/metadata/details/story_details/part-m-00000", "r")
for line in f:
  writerID, storyID, categoryID, rating = [x.rstrip() for x in line.split("\t")]
  categories[storyID] = categoryID
f.close 

class Cat:
#    def __init__(self, freq_s, freq_h, freq_her, freq_him, freq_her_pos, freq_his, freq_sobj, freq_hobj, tot_s, tot_h, tot_her, tot_him, tot_her_pos, tot_his, pmi_h, pmi_s, pmi_her, pmi_him, pmi_her_pos, pmi_his, pmi_sobj, pmi_hobj):
  freq_h = defaultdict(int)
  freq_s = defaultdict(int)
  freq_her = defaultdict(int)
  freq_him = defaultdict(int)
  freq_her_pos = defaultdict(int)
  freq_his = defaultdict(int)
  freq_sobj = defaultdict(int)
  freq_hobj = defaultdict(int)
  pmi_h = defaultdict(float)
  pmi_s = defaultdict(float)
  pmi_her = defaultdict(float)
  pmi_him = defaultdict(float)
  pmi_her_pos = defaultdict(float)
  pmi_his = defaultdict(float)
  pmi_sobj = defaultdict(float)
  pmi_hobj = defaultdict(float)
  tot_s = 0.0
  tot_h = 0.0
  tot_her = 0.0
  tot_him = 0.0
  tot_her_pos = 0.0
  tot_his = 0.0

cats = {}
for x in range (1, 25):
  cats[x] = Cat()

nlp = spacy.en.English()
f = open("small.pmis.txt", "w")

#x = [1,2,3]
#y = [z*z for z in x if z > 1]

def findObjFreq(tk, freq):
  for x in tk.children:
     if(x.pos_ == "NOUN"):
        freq[x.lemma_] += 1
        
def countOccur(chapter, cat):
  for sen in chapter.split("." or "!" or "?"):
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
      
        if(tk.pos_ == "VERB"):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "she"):
                   cats[cat].tot_s += 1
                   cats[cat].freq_s[tk.lemma_] +=1
                   findObjFreq(tk, cats[cat].freq_sobj)
                elif (x.lower_ == "he"):
                   cats[cat].tot_h += 1
                   cats[cat].freq_h[tk.lemma_] +=1
                   findObjFreq(tk, cats[cat].freq_hobj)
                elif (x.lower_ == "her"):
                   cats[cat].tot_her += 1
                   cats[cat].freq_her[tk.lemma_] +=1
                elif (x.lower_ == "him"):
                   cats[cat].tot_him += 1
                   cats[cat].freq_him[tk.lemma_] +=1
                   
        elif(tk.pos_ == "NOUN"):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "her"):
                   cats[cat].tot_her_pos += 1
                   cats[cat].freq_her_pos[tk.lemma_] +=1
                elif (x.lower_ == "his"):
                   cats[cat].tot_his += 1
                   cats[cat].freq_his[tk.lemma_] +=1
                    
    except UnicodeDecodeError:
      pass

def calcPMI(pron, word, freq, tot):
  if(tot != 0 and freq[word] != 0):
     wordGivenPron = freq[word]/tot
     pronGivenWord = (2**(nlp.vocab[pron].prob) * wordGivenPron) /2**(nlp.vocab[unicode(word)].prob)
     x = pronGivenWord/2**(nlp.vocab[pron].prob)
     pmi = math.log(x)
  else:
     pmi = 0.0
  return pmi
  
def calcAllPMIs(pron, freq, tot, pmi):
  for key in freq:
     pmi[key] += 1
  for k,v in freq.iteritems():
     pmi[k] = calcPMI(pron, k, freq, tot)

def calcPMIs(cat):
  calcAllPMIs(u'she', cats[cat].freq_s, cats[cat].tot_s, cats[cat].pmi_s)
  calcAllPMIs(u'he', cats[cat].freq_h, cats[cat].tot_h, cats[cat].pmi_h)
  calcAllPMIs(u'her', cats[cat].freq_her, cats[cat].tot_her, cats[cat].pmi_her)
  calcAllPMIs(u'him', cats[cat].freq_him, cats[cat].tot_him, cats[cat].pmi_him)
  calcAllPMIs(u'her', cats[cat].freq_her_pos, cats[cat].tot_her_pos, cats[cat].pmi_her_pos)
  calcAllPMIs(u'his', cats[cat].freq_his, cats[cat].tot_his, cats[cat].pmi_his)
  calcAllPMIs(u'she', cats[cat].freq_sobj, cats[cat].tot_s, cats[cat].pmi_sobj)
  calcAllPMIs(u'he', cats[cat].freq_hobj, cats[cat].tot_h, cats[cat].pmi_hobj)

def putInFile():
  for k in cats:
     pickle.dump(k, f)
     pickle.dump(cats[k].pmi_h, f)
     pickle.dump(cats[k].pmi_s, f)
     pickle.dump(cats[k].pmi_her, f)
     pickle.dump(cats[k].pmi_him, f)
     pickle.dump(cats[k].pmi_her_pos, f)
     pickle.dump(cats[k].pmi_his, f)
     pickle.dump(cats[k].pmi_sobj, f)
     pickle.dump(cats[k].pmi_hobj, f)
     #pickle.dump(tot_h, f)
     #pickle.dump(tot_s, f)
     #pickle.dump(tot_her, f)
     #pickle.dump(tot_him, f)
     #pickle.dump(tot_her_pos, f)
     #pickle.dump(tot_his, f)


def findPMIForCat(chapter, cat):
  countOccur(chapter, cat)
  calcPMIs(cat)

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  storyid = stories[id_]
  cat = int(categories[storyid])
  findPMIForCat(chapter, cat)

putInFile()     

f.close()

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
##  for word in largeAndPos:
##     print (word)
##     print ("Frequency for ", prons, pmis[word], "Frequency for ", pronh, pmih[word])  
##  print ("Max for ", prons, pronh, "is", mx)
##  print ("Frequency for ", prons, pmis[mx], "Frequency for ", pronh, pmih[mx])
#
#calcPMIsAndFindMax(u'she', freq_s, tot_s, pmi_s, u'he', freq_h, tot_h, pmi_h)
#calcPMIsAndFindMax(u'her', freq_her, tot_her, pmi_her, u'him', freq_him, tot_him, pmi_him) 
#calcPMIsAndFindMax(u'her', freq_her_pos, tot_her_pos, pmi_her_pos, u'his', freq_his, tot_his, pmi_his) 
#calcPMIsAndFindMax(u'she', freq_sobj, tot_s, pmi_sobj, u'he', freq_hobj, tot_h, pmi_hobj)  

 
#def queryForVerbFreq(freq_s, tot_s, freq_h, tot_h, freq_her, tot_her, freq_him, tot_him):
#   verb = ""      
#   while True:
#     verb = input("Enter a verb (Quit to quit, remember the quotation marks!): ")
#     if(verb == "Quit"): return
#     print ("Frequency for she: ", pmi_s[verb], "Frequency for he: ", pmi_h[verb])
#     print ("Frequency for her: ", pmi_her[verb], "Frequency for him: ", pmi_him[verb])
#     
#def queryForNounFreq(freq_her_pos, tot_her_pos, freq_his, tot_his, freq_sobj, tot_s, freq_hobj, tot_h):
#   noun = ""
#   while True:
#      noun = input("Enter a noun (Quit to quit, remember the quotation marks!): ")
#      if(noun == "Quit"): return
#      print ("Frequency for she: ", pmi_sobj[noun], "Frequency for he: ", pmi_hobj[noun])
#      print ("Frequency for her: ", pmi_her_pos[noun], "Frequency for his: ", pmi_his[noun])
#      
#queryForVerbFreq(freq_s, tot_s, freq_h, tot_h, freq_her, tot_her, freq_him, tot_him)
#queryForNounFreq(freq_her_pos, tot_her_pos, freq_his, tot_his, freq_sobj, tot_s, freq_hobj, tot_h)