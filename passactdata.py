import os
dir = os.path.dirname(__file__)

verbs = {}

f = open(os.path.join(dir,"passactverbs.txt"), 'r')
for line in f:
  verb, typ, freq = [x.rstrip() for x in line.split("\t")]
  verbs[verb] = typ

f.close
