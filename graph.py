import matplotlib.pyplot as plt
import numpy as np

def makehistogram(arr, binnum):
   plt.hist(arr, bins = binnum)
   plt.show()

def getGenres():
   genre = {}
   f = open("/home/ubuntu/ebs/bias/metadata/categories/categories/part-m-00000", 'r')
   for line in f:
     catID, cat = [x.rstrip() for x in line.split("\t")]
     catnum = int(catID)
     genre[catnum] = cat
   genre[0] = "Other"
   return genre

def multhisto(row, col, n, arrs, binnum, ylim):  
   fig, axes = plt.subplots(nrows=row, ncols=col, sharex='col', sharey='row')
   if(n == 25):
      genre = getGenres()
   for i, ax in enumerate(axes.flat, start=0):
       if(i >= n): arrs[i] = [0]
       if(len(arrs[i]) == 0): arrs[i] = [0]
       if(n == 25 and (i in genre)):
          ax.set_title(genre[i])
       else:
          ax.set_title('Group {}'.format(i))
       ax.hist(arrs[i], bins = binnum, range = [-6, 6])
       ax.set_ylim(0, ylim)
#       ax.set_xlabel('Difference in PMIs')
#       ax.set_ylabel('Num Words')
   
   #fig.tight_layout()   
   plt.show()

