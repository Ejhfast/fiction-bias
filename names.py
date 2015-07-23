from sets import Set

def readNames(filename):
  f = open(filename, 'r')
  names = Set([])
  for line in f:
    name, freq, index, url = [x.rstrip() for x in line.split(",")]
    name = name.replace("\"","")
    names.add(name.lower())
  return names

malnames = readNames("/home/ubuntu/ebs/male-names-freq.csv")
femnames = readNames("/home/ubuntu/ebs/female-names-freq.csv")

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
