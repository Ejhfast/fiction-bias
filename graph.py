import matplotlib.pyplot as plt
import numpy as np

def makehistogram(arr, binnum):
   plt.hist(arr, bins = binnum)
   plt.show()

def multhisto(row, col, n, arrs, binnum):  
   fig, axes = plt.subplots(nrows=row, ncols=col)

   for i, ax in enumerate(axes.flat, start=0):
       if(i >= n): break
       ax.set_title('Group {}'.format(i))
       ax.hist(arrs[i], bins = binnum)
       ax.set_xlabel('Difference in PMIs')
       ax.set_ylabel('Num Words')
   
   fig.tight_layout()   
   plt.show()

