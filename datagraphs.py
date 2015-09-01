import numpy as np
import graph
import charcountsread
import actpass
import dialogread
from sets import Set

from bokeh.plotting import figure, output_file, show, VBox

genFTot = charcountsread.genFTot
genMTot = charcountsread.genMTot
genFTh = charcountsread.genFTh
genMTh = charcountsread.genMTh
genFOn = charcountsread.genFOn
genMOn = charcountsread.genMOn

genFAct = actpass.genFAct
genFPass = actpass.genFPass
genMAct = actpass.genMAct
genMPass = actpass.genMPass

genFDial = dialogread.genFTot
genMDial = dialogread.genMTot
genFUn = dialogread.genFUn
genMUn = dialogread.genMUn
genFInit = dialogread.genFInit
genMInit = dialogread.genMInit

# EXERCISE: output static HTML file
output_file('bigdatagraphs.html')

TOOLS = 'save'

def graphPer(genF, genM, titleName, h):
   female = np.array([genF[name] for name in genF], dtype=np.float)
   male = np.array([genM[name] for name in genM], dtype=np.float)
   # create a figure()
   p1 = figure(title=titleName, tools=TOOLS,
               x_range=list(genF.keys()), y_range=[0, max(female + male)],
               background_fill='white', plot_width=1600, plot_height = h
       )
   
   # use the `rect` renderer to display stacked bars of the medal results. Note
   # that we set y_range explicitly on the first renderer
   #p1.rect(x=genF, y=bronze/2, width=0.8, height=bronze, color="#CD7F32", alpha=0.6)
   p1.rect(x=list(genF.keys()), y=male/2, width=0.8, height=male, color="green", alpha=0.6)
   
   # EXERCISE: add a `rect` renderer to stack the orange medal results
   p1.rect(x=list(genF.keys()), y=male + female/2, width=0.8, height=female, color="orange", alpha=0.6)
   
   # EXERCISE: use grid(), axis(), etc. to style the plot. Some suggestions:
   #   - remove the grid lines
   #   - change the major label standoff, and major_tick_out values
   #   - make the tick labels smaller
   #   - set the x-axis orientation to vertical, or angled
   p1.xgrid.grid_line_color = None
   p1.axis.major_label_text_font_size = "24pt"
   p1.axis.major_label_standoff = 0
   p1.xaxis.major_label_orientation = np.pi/3
   p1.xaxis.major_label_standoff = 6
   p1.xaxis.major_tick_out = 0
   return p1

   # show the plots arrayed in a VBox

def graphNotStacked(genF, genM, titleName, maxgen):   
   female = np.array([genF[name] for name in genF], dtype=np.float)
   male = np.array([genM[name] for name in genM], dtype=np.float)
   if maxgen == "female":
     maxarr = female
   else:
     maxarr = male
   p2 = figure(title=titleName, tools=TOOLS, x_range=list(genF.keys()), y_range=[0, max(maxarr) + .1], background_fill='white', plot_width=1600, plot_height=600)
   # Categorical percentage coordinates can be used for positioning/grouping
   dial_fem = [c+":0.3" for c in genF.keys()]
   dial_mal = [c+":0.5" for c in genM.keys()]
   #countries_orange = [c+":0.7" for c in countries]
   
   # EXERCISE: re create the medal plot, but this time:
   #   - do not stack the bars on the y coordinate
   #   - use countries_orange, etc. to positions the bars on the x coordinate
   p2.rect(x=dial_mal, y=male/2, width=0.2, height=male, color="green", alpha=0.6)
   p2.rect(x=dial_fem, y=female/2, width=0.2, height=female, color="orange", alpha=0.6)
   
   p2.xgrid.grid_line_color = None
   p2.axis.major_label_text_font_size = "24pt"
   p2.axis.major_label_standoff = 0
   p2.xaxis.major_label_orientation = np.pi/3
   p2.xaxis.major_label_standoff = 6
   p2.xaxis.major_tick_out = 0
   return p2
   
p1 = graphPer(genFTot, genMTot, "Total Character Percentages (orange = Female, green = Male)", 1200)
p2 = graphPer(genFTh, genMTh, "Top 3 Main Character Percentages (orange = Female, green = Male)", 1200)
p3 = graphPer(genFOn, genMOn, "Main Character Percentages (orange = Female, green = Male)", 1200)
p4 = graphPer(genFPass, genFAct, "Fem. Active and Passive Percentages (orange = Pass., green = Act.)", 800)
p5 = graphPer(genMPass, genMAct, "Male Active and Passive Percentages (orange = Pass., green = Act.)", 800)
p6 = graphNotStacked(genFDial, genMDial, "Percent Dialogue Ratio to Char (orange = Female, green = Male)", "male")
p7 = graphNotStacked(genFUn, genMUn, "Unique Speaking Char. Perc. (orange = Female, green = Male)", "male")
p8 = graphNotStacked(genFInit, genMInit, "Char. Initiating Dialogue Per. (orange = Female, green = Male)", "male")

show(VBox(p1, p2, p3, p4, p5, p6, p7, p8))