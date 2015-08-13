from sets import Set
import os
dir = os.path.dirname(__file__)

f = open (os.path.join(dir,"genderedterms.txt"), 'r')

malnames = Set([])
femnames = Set([])

for line in f:
  name, gender = [x.rstrip() for x in line.split(" ")]
  if(gender == 'f'):
    femnames.add(name)
  else:
    malnames.add(name)

def ismaleterm(name):
  if (name in malnames):
     return True
  else:
     return False

def isfemaleterm(name):
  if (name in femnames):
     return True
  else:
     return False
