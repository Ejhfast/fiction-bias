import fileinput
from collections import defaultdict
import spacy.en

freq_h = defaultdict(int)
freq_s = defaultdict(int)
#freq_h["rando"] += 1

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
  for sen in chapter.split("."):
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
        if(tk.pos_ == "VERB"):
           for x in tk.children:
              if(x.pos_ == "PRON"):
                if (x.lower_ == "she"):
                   # print (tk.lower_, x.lower_)
                   freq_s[tk.lower_] +=1
                   # print freq_s[tk.lower_]
                elif (x.lower_ == "he"):
                   # print (tk.lower_, x.lower_)
                   freq_h[tk.lower_] +=1
                   # print freq_h[tk.lower_]
             
            
          #print(tk.pos_, tk.lemma_, tk.lemma, tk.lower_, tk.lower, tk.dep_, [x.lower_ for x in tk.children])
    except UnicodeDecodeError:
      pass