verbs = {}

f = open("passactverbs.txt", 'r')
for line in f:
  verb, typ, freq = [x.rstrip() for x in line.split("\t")]
  verbs[verb] = typ

f.close
