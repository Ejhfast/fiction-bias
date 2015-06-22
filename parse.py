import fileinput
from collections import defaultdict
import spacy.en

freq_h = defaultdict(int)

freq_h["rando"] += 1

# for k,v in freq_h.iteritems():
  # iterate over dictionary keys, values

nlp = spacy.en.English()

x = [1,2,3]
y = [z*z for z in x if z > 1]

for line in fileinput.input():
  id_, chapter = [x.rstrip() for x in line.split("\t")]
  id_ = int(id_)
  for sen in chapter.split("."):
    try:
      tokens = nlp(unicode(sen),tag=True,parse=True)
      for tk in tokens:
        #if(tk.pos_ == "VERB"):
        print(tk.pos_, tk.lemma_, tk.lemma, tk.orth_, tk.orth, tk.dep_, [x.orth_ for x in tk.children])
    except UnicodeDecodeError:
      pass
