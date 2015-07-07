import fileinput
from collections import defaultdict
import spacy.en
import math
import cPickle as pickle

LARGEANDPOS = 1

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
 
 # for k,v in freq_h.iteritems():
   # iterate over dictionary keys, values
 
nlp = spacy.en.English()
f = open("pm00000.pmis.txt", "w")
 
 #x = [1,2,3]
 #y = [z*z for z in x if z > 1]
 
def findObjFreq(tk, freq):
  for x in tk.children:
     if(x.pos_ == "NOUN"):
        freq[x.lemma_] += 1

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  id_ = int(id_)
  for sen in chapter.split("." or "!" or "?"):
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
      
        if(tk.pos_ == "VERB"):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "she"):
                   tot_s += 1
                   freq_s[tk.lemma_] +=1
                   findObjFreq(tk, freq_sobj)
                elif (x.lower_ == "he"):
                   tot_h += 1
                   freq_h[tk.lemma_] +=1
                   findObjFreq(tk, freq_hobj)
                elif (x.lower_ == "her"):
                   tot_her += 1
                   freq_her[tk.lemma_] +=1
                elif (x.lower_ == "him"):
                   tot_him += 1
                   freq_him[tk.lemma_] +=1
                   
        elif(tk.pos_ == "NOUN"):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "her"):
                   tot_her_pos += 1
                   freq_her_pos[tk.lemma_] +=1
                elif (x.lower_ == "his"):
                   tot_his += 1
                   freq_his[tk.lemma_] +=1
                    
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
      
calcAllPMIs(u'she', freq_s, tot_s, pmi_s)
calcAllPMIs(u'he', freq_h, tot_h, pmi_h)
calcAllPMIs(u'her', freq_her, tot_her, pmi_her)
calcAllPMIs(u'him', freq_him, tot_him, pmi_him)
calcAllPMIs(u'her', freq_her_pos, tot_her_pos, pmi_her_pos)
calcAllPMIs(u'his', freq_his, tot_his, pmi_his)
calcAllPMIs(u'she', freq_sobj, tot_s, pmi_sobj)
calcAllPMIs(u'he', freq_hobj, tot_h, pmi_hobj)

pickle.dump(pmi_h, f)
pickle.dump(pmi_s, f)
pickle.dump(pmi_her, f)
pickle.dump(pmi_him, f)
pickle.dump(pmi_her_pos, f)
pickle.dump(pmi_his, f)
pickle.dump(pmi_sobj, f)
pickle.dump(pmi_hobj, f)
#pickle.dump(tot_h, f)
#pickle.dump(tot_s, f)
#pickle.dump(tot_her, f)
#pickle.dump(tot_him, f)
#pickle.dump(tot_her_pos, f)
#pickle.dump(tot_his, f)
 
 f.close()
