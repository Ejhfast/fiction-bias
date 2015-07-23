verbs = {}

f = open("/home/ubuntu/ebs/passactverbs.txt", 'r')
for line in f:
  verb, typ, freq = [x.rstrip() for x in line.split("\t")]
  verbs[verb] = typ

print(verbs)
f.close
