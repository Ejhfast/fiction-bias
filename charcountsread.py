f = open('charcountstemp.txt', 'r')
fw = open('charcountsdata.txt', 'w')

genFTot = {}
genMTot = {}
genFTh = {}
genMTh = {}
genFOn = {}
genMOn = {}

def calcNPrint(fem, mal, genF, genM, name, rat, title):
  femPerc = float(fem)/(float(mal) + float(fem))  
  malPerc = float(mal)/(float(mal) + float(fem))
  genF[name] = femPerc
  genM[name] = malPerc
  fw.write(title + "Percent Female: " + str(femPerc) + "\tPercent Male: " + str(malPerc) + "\tRatio Fem/Mal: " + rat + "\n")

for line in f:
  name, femTot, malTot, ratTot, femTh, malTh, ratTh, femOn, malOn, ratOn = [x.rstrip() for x in line.split(" ")]
  fw.write(name + "\n")
  calcNPrint(femTot, malTot, genFTot, genMTot, name, ratTot, "Total Characters: ")
  calcNPrint(femTh, malTh, genFTh, genMTh, name, ratTh, "Top 3 Main Characters: ")
  calcNPrint(femOn, malOn, genFOn, genMOn, name, ratOn, "Main Characters: ")
  fw.write("\n")
f.close

