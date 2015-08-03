import cPickle as pickle
import spacy.en
from collections import defaultdict

nlp = spacy.en.English()

liwcp = open("/home/ubuntu/fast_liwc.pkl", 'r')
f = open("gendereddialogsmall.txt", 'r')
fwr = open("liwcpercents.txt", 'w')

liwc = pickle.load(liwcp)
fem = defaultdict(int)
male = defaultdict(int)

def addToDict(dict1, dict2):
  for key in dict2:
     dict1[key] += dict2[key]

for line in f:
  quote, gender, cat, storyid = [x.rstrip() for x in line.split("\t")]
  try:
    for word in nlp(unicode(quote), parse=False): 
       if(word.orth_ in liwc):
          if(gender == "female"):
             addToDict(fem, liwc[word.orth_])
          elif(gender == "male"):
             addToDict(male, liwc[word.orth_])

     
  except UnicodeDecodeError:
     pass

#ratio = defaultdict(float)
#for key in fem:
#   ratio[key] = float[fem[key]]/float(male[key])

def countTotal(dic):
   total = 0
   for key in dic:
     total += dic[key]
   return total

def findPerc(dic, total):
   result = {}
   for key in dic:
      result[key] = dic[key]/float(total)
   return result

def writePerc(dic):
   for key in dic:
      fwr.write(key + " " + str(dic[key]) + "\n")

femTotal = countTotal(fem)
femPerc = findPerc(fem, femTotal)
writePerc(femPerc)
malTotal = countTotal(male)
malPerc = findPerc(male, malTotal)
writePerc(malPerc)
