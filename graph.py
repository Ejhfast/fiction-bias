import matplotlib.pyplot as plt

def makehistogram(arr, binnum):
   plt.hist(arr, bins = binnum)
   plt.show()