from sets import Set

f = open("/home/ubuntu/ebs/names.txt", 'r')
malnames = Set([])
femnames = Set([])
for line in f:
  freq, femname, malname = [x.rstrip() for x in line.split("\t")]
  femnames.add(femname.lower())
  malnames.add(malname.lower())

duplicate = Set([])

for name in femnames:
  if (name in malnames):
    duplicate.add(name)

for name in duplicate:
  femnames.remove(name)
  malnames.remove(name)

print femnames
print malnames
print duplicate

def ismalename(name):  
  if (name in malnames):
     return True
  else:
     return False     

def isfemalename(name):
  #print (name)
  if (name in femnames):
     return True
  else:
     return False  
