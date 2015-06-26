import fileinput
from collections import defaultdict
import spacy.en
import math

freq_h = defaultdict(int)
freq_s = defaultdict(int)
freq_her = defaultdict(int)
freq_him = defaultdict(int)
tot_s = 0.0
tot_h = 0.0
tot_her = 0.0
tot_him = 0.0

# for k,v in freq_h.iteritems():
  # iterate over dictionary keys, values

nlp = spacy.en.English()

#x = [1,2,3]
#y = [z*z for z in x if z > 1]

#def updateVerbFreq(tk, freq):
#  for x in tk.children:
#    if(x.pos_ == "VERB"):
#      print (tk.lower_, x.lower_)
#      freq[x.lower_] +=1

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
                   # print (tk.lower_, x.lower_)
                   tot_s += 1
                   freq_s[tk.lemma_] +=1
                   # print freq_s[tk.lower_]
                elif (x.lower_ == "he"):
                   # print (tk.lower_, x.lower_)
                   tot_h += 1
                   freq_h[tk.lemma_] +=1
                   # print freq_h[tk.lower_]
                elif (x.lower_ == "her"):
                   tot_her += 1
                   freq_her[tk.lemma_] +=1
                elif (x.lower_ == "him"):
                   tot_him += 1
                   freq_him[tk.lemma_] +=1
             
#         if(tk.pos_ == "PRON"):
#            parent = tk.parent
#            print(parent)
            # print(tk.pos_, tk.lemma_, tk.lemma, tk.lower_, tk.lower, tk.dep_, [x.lower_ for x in tk.children])
    except UnicodeDecodeError:
      pass


def calcPMI(pron, verb, freq, tot):
  if(tot != 0 and freq[verb] != 0):
     verbGivenPron = freq[verb]/tot
     pronGivenVerb = (2**(nlp.vocab[pron].prob) * verbGivenPron) /2**(nlp.vocab[unicode(verb)].prob)
     x = pronGivenVerb/2**(nlp.vocab[pron].prob)
     pmi = math.log(x)
  else:
     pmi = 0
  return pmi

verb = ""      
while(verb != "Quit"):
  verb = input("Enter a verb (Quit to quit, remember the quotation marks!): ")
  pmi_she = calcPMI(u'she', verb, freq_s, tot_s)
  pmi_he = calcPMI(u'he', verb, freq_h, tot_h)
  pmi_her = calcPMI(u'her', verb, freq_her, tot_her)
  pmi_him = calcPMI(u'him', verb, freq_him, tot_him)
#  verbGivenShe = freq_s[verb]/tot_s
#  verbGivenHe = freq_h[verb]/tot_h
#  sheGivenVerb = (2**(nlp.vocab[u'she'].prob) * verbGivenShe) /2**(nlp.vocab[unicode(verb)].prob)
#  heGivenVerb = (2**(nlp.vocab[u'he'].prob) * verbGivenHe) /2**(nlp.vocab[unicode(verb)].prob)
#  pmi_she = sheGivenVerb/2**(nlp.vocab[u'she'].prob)
#  pmi_he = heGivenVerb/2**(nlp.vocab[u'he'].prob)
  # print ("Frequency for female: ", freq_s[verb]/tot_s, "Frequency for male: ", freq_h[verb]/tot_h)
  print ("Frequency for she: ", pmi_she, "Frequency for he: ", pmi_he, "Frequency for her: ", pmi_her, "Frequency for him: ", pmi_him)