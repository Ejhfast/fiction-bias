import numpy as np
import graph
import charcountsread
import actpass

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

# EXERCISE: output static HTML file
output_file('charcountsgraphs.html')

def graphPer(genF, genM, titleName):
   female = np.array([genF[name] for name in genF], dtype=np.float)
   male = np.array([genM[name] for name in genM], dtype=np.float)
   # create a figure()
   p1 = figure(title=titleName, tools="",
               x_range=list(genF.keys()), y_range=[0, max(female + male)],
               background_fill='#59636C', plot_width=800
       )
   
   # use the `rect` renderer to display stacked bars of the medal results. Note
   # that we set y_range explicitly on the first renderer
   #p1.rect(x=genF, y=bronze/2, width=0.8, height=bronze, color="#CD7F32", alpha=0.6)
   p1.rect(x=list(genF.keys()), y=male/2, width=0.8, height=male, color="silver", alpha=0.6)
   
   # EXERCISE: add a `rect` renderer to stack the gold medal results
   p1.rect(x=list(genF.keys()), y=male + female/2, width=0.8, height=female, color="gold", alpha=0.6)
   
   # EXERCISE: use grid(), axis(), etc. to style the plot. Some suggestions:
   #   - remove the grid lines
   #   - change the major label standoff, and major_tick_out values
   #   - make the tick labels smaller
   #   - set the x-axis orientation to vertical, or angled
   p1.xgrid.grid_line_color = None
   p1.axis.major_label_text_font_size = "8pt"
   p1.axis.major_label_standoff = 0
   p1.xaxis.major_label_orientation = np.pi/3
   p1.xaxis.major_label_standoff = 6
   p1.xaxis.major_tick_out = 0
   return p1

   # show the plots arrayed in a VBox
   
p1 = graphPer(genFTot, genMTot, "Total Character Percentages (Gold = Female, Silver = Male)")
p2 = graphPer(genFTh, genMTh, "Top 3 Main Character Percentages (Gold = Female, Silver = Male)")
p3 = graphPer(genFOn, genMOn, "Main Character Percentages (Gold = Female, Silver = Male)")
p4 = graphPer(genFPass, genFAct, "Female Active and Passive Percentages (Gold = Pass., Silver = Act.)")
p5 = graphPer(genMPass, genMAct, "Male Active and Passive Percentages (Gold = Pass., Silver = Act.)")

show(VBox(p1, p2, p3, p4, p5))