import charcountsread

f = open('dialog.txt', 'r')
fw = open('dialogdata.txt', 'w')

genFCTot = charcountsread.genFTot
genMCTot = charcountsread.genMTot

genFTot = {}
genMTot = {}
genFUn = {}
genMUn = {}
genFInit = {}
genMInit = {}

def calcNPrint(fem, mal, genF, genM, name, rat, title):
  femPerc = float(fem)/(float(mal) + float(fem))  
  malPerc = float(mal)/(float(mal) + float(fem))
  femRat = femPerc/genFCTot[name]
  malRat = malPerc/genMCTot[name]
  normRat = femRat/malRat
  genF[name] = femRat
  genM[name] = malRat
  fw.write(title + "\n" + "Percent Female: " + str(femPerc) + "\tRatio to female characters: " + str(femRat) +  "\n" + "Percent Male: " + str(malPerc) + "\tRatio to male characters: " + str(malRat) + "\n" + "Ratio Fem/Mal: " + rat + "\tNorm Ratio Fem/Male: " + str(normRat) + "\n")


for line in f:
  name, femTot, malTot, ratTot, femUn, malUn, ratUn, femInit, malInit, ratInit = [x.rstrip() for x in line.split(" ")]
  fw.write(name + "\n")
  calcNPrint(femTot, malTot, genFTot, genMTot, name, ratTot, "Percent for all Dialogue: ")
  calcNPrint(femUn, malUn, genFUn, genMUn, name, ratUn, "Unique Speakers: ")
  calcNPrint(femInit, malInit, genFInit, genMInit, name, ratInit, "Initiating Speakers: ")
  fw.write("\n")
f.close