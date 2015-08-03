import charcountsread

f = open('dialogtest.txt', 'r')
fw = open('dialogdata.txt', 'w')

genFCTot = charcountsread.genFTot
genMCTot = charcountsread.genMTot

genFTot = {}
genMTot = {}
genFUn = {}
genMUn = {}

def calcNPrint(fem, mal, genF, genM, name, rat, title):
  femPerc = float(fem)/(float(mal) + float(fem))  
  malPerc = float(mal)/(float(mal) + float(fem))
  femRat = femPerc/genFCTot[name]
  malRat = malPerc/genMCTot[name]
  normRat = femRat/malRat
  genF[name] = femRat
  genM[name] = malRat
  fw.write("Percent Female: " + str(femPerc) + "\tRatio to female characters: " + str(femRat) +  "\n" + "Percent Male: " + str(malPerc) + "\tRatio to male characters: " + str(malRat) + "\n" + "Ratio Fem/Mal: " + rat + "\tNorm Ratio Fem/Male: " + str(normRat) + "\n")


for line in f:
  name, femTot, malTot, ratTot, femUn, malUn, ratUn = [x.rstrip() for x in line.split(" ")]
  fw.write(name + "\n")
  calcNPrint(femTot, malTot, genFTot, genMTot, name, ratTot, "Percent for all Dialogue: ")
#  calcNPrint(femUn, malUn, genFUn, genMUn, name, ratUn, "Unique Speakers: ")
  fw.write("\n")
f.close