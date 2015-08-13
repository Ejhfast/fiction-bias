from sets import Set
import spacy.en

f = open("speakerverbs.txt", 'r')
# fi2 = open("/home/ubuntu/ebs/bias/actualspeakerverbs.txt", 'w')

nlp = spacy.en.English()

speakerverbs = Set([])

#for line in fi:
#   num, verb = [x.rstrip() for x in line.split(". ")]
#   tokens = nlp(unicode(verb),tag=True,parse=True)
#   for tk in tokens:
#      fi2.write(tk.lemma_ + "\n")

speakerverbs.add("say")

for line in f:
   word, num = [x.rstrip() for x in line.split("\n")]
   speakerverbs.add(word)

def speakerverb(verb):
   if(verb in speakerverbs):
      return True
   else:
      return False
