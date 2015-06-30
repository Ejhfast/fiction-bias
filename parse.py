import fileinput
from collections import defaultdict
import spacy.en
import math

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
     pmi = 0
  return pmi

def calcAllPMIs(pron, freq, tot, pmi):
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

def queryForVerbFreq(freq_s, tot_s, freq_h, tot_h, freq_her, tot_her, freq_him, tot_him):
   verb = ""      
   while True:
     verb = input("Enter a verb (Quit to quit, remember the quotation marks!): ")
     if(verb == "Quit"): return
#     pmi_she = calcPMI(u'she', verb, freq_s, tot_s)
#     pmi_he = calcPMI(u'he', verb, freq_h, tot_h)
#     pmi_her = calcPMI(u'her', verb, freq_her, tot_her)
#     pmi_him = calcPMI(u'him', verb, freq_him, tot_him)
     print ("Frequency for she: ", pmi_s[verb], "Frequency for he: ", pmi_h[verb])
     print ("Frequency for her: ", pmi_her[verb], "Frequency for him: ", pmi_him[verb])
     
def queryForNounFreq(freq_her_pos, tot_her_pos, freq_his, tot_his, freq_sobj, tot_s, freq_hobj, tot_h):
   noun = ""
   while True:
      noun = input("Enter a noun (Quit to quit, remember the quotation marks!): ")
      if(noun == "Quit"): return
#      pmi_her_pos = calcPMI(u'her', noun, freq_her_pos, tot_her_pos)
#      pmi_his = calcPMI(u'his', noun, freq_his, tot_his)
#      pmi_sobj = calcPMI(u'she', noun, freq_sobj, tot_s)
#      pmi_hobj = calcPMI(u'he', noun, freq_hobj, tot_h)
      print ("Frequency for she: ", pmi_sobj[noun], "Frequency for he: ", pmi_hobj[noun])
      print ("Frequency for her: ", pmi_her_pos[noun], "Frequency for his: ", pmi_his[noun])
      
queryForVerbFreq(freq_s, tot_s, freq_h, tot_h, freq_her, tot_her, freq_him, tot_him)
queryForNounFreq(freq_her_pos, tot_her_pos, freq_his, tot_his, freq_sobj, tot_s, freq_hobj, tot_h)