# Loading all modules to fix this project
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import datetime
import os

#Get path to python file
new_path = (os.path.dirname(__file__)).replace("\\","/")

# Taking in file path to load excel file 
file_path = (input('Enter the file path to the excel sheet:            '))
file_name, file_extension = os.path.splitext(file_path)

# Checking the file extension to make sure code doesn't break
while file_extension not in [".csv"]:
	print("FileExtensionError. File extension should be: \".csv\" such as file_name.csv")
	file_path = (input('Enter the file path to the excel sheet again:            '))
	file_name, file_extension = os.path.splitext(file_path)

# Continue here when above is passed
path = file_path
file = open(path, encoding='utf-8', newline='')
file = pd.read_csv(path)
my_list = []

for row in file.values:
	my_list.append(list(row))

#Store Sieve Sizes and %Passing for all Sieves
data = []     
for row in my_list:
	#sieve_size, wt of sieve, wt of sieve+sample, wt retained, %retained, cumm. retained, %passing
	sieve_size = float(row[0])
	cumm_ret = float(row[-2])
	passing = float(row[-1])
	data.append((sieve_size, cumm_ret, passing))

#Storing %passing for sieve sizes: 5mm, 2mm, 0.425 and 0.075
data_value = []      
for row in data:
	if row[0] in [5, 4.75, 2, 0.425, 0.075]:
		data_value.append(row[-1])

#Storing %cumm_retained for sieve sizes: 5mm, 2.36mm, 1.18mm, 0.6mm, 0.3mm and 0.15mm
data_value_ret = []      
for row in data:
	if row[0] in [5, 4.75, 2.36, 1.18, 0.6, 0.3, 0.15]:
		data_value_ret.append(row[-2])

sum = 0
for i in range(0,len(data_value_ret)):
	sum += data_value_ret[i]

finess_modulus = round(sum/100,2)

#AASHTO Classification list 
AASHTO = [
        ("A-1-a: Stone Fragments (Gravel and Sand). Rating: Excellent to Good", "A-1-b: Stone Fragments (Gravel and Sand). Rating: Excellent to Good"),
        "A-3: Fine Sand. Rating: Excellent to Good",
        ("A-2-4: Silty or Clayey Gravel Sand. Rating: Good", 
         "A-2-5: Silty or Clayey Gravel Sand. Rating: Good", 
         "A-2-6: Silty or Clayey Gravel Sand. Rating: Good", 
         "A-2-7: Silty or Clayey Gravel Sand. Rating: Good"),
        "A-4: Silty Soil. Rating: Fair", "A-5: Silty Soil. Rating: Fair",
        "A-6: Silty Soil. Rating: Fair",
        ("A-7-5: Clayey Soil. Rating: Poor", "A-7-6: Clayey Soil. Rating: Poor")
]

#USCS Classification list
USCS = [
        ("GW: Well-graded gravels and gravel-sand mixtures, little or no fines", 
         "GP: Poorly-graded gravels and gravel-sand mixtures, little or no fines", 
         "GM: Silty gravels, gravel-sand-silt mixtures", "GC: Clayey gravels, gravel-sand-clay mixtures",
         "GM - GC: Silty gravel with clay", "GW - GM: Well graded gravel with silt"
         ),
        ("SW: Well-graded sands and gravelly sands, little or no fines", 
         "SP: Poorly-graded sands and gravelly sands, little or no fines", 
         "SM: Silty sands", "SC: Clayey sands", 
         "SM - SC: Silty sand with clay",
         "SP - SC: Poorly graded sand with clay"),
        ("CL: Inorganic Clays of low to medium Plasticity",
         "ML: Inorganic Silts, very fine sand, Rock Flour of medium to low plasticity or\n OL: Organic Silt and Organic Silt Clay of low Plasticity",
         "CL - ML: Silty Clay with Sand"),
        ("CH: Inorganic Clay of high Plasticty", 
         "MH: Inorganic Silt, Micaceous, Diatomaceous fine sand or silt of high Plasticity or\n OH: Organic Clay of medium to high Plasticity")
]

#Storing x and y values to plot graph

# Store x-axis values for plotting
x = [] 
for row in data:
	x.append(row[0])

#Store y-axis values for plotting
y = []
for row in data:
	y.append(row[-1])

# Turning x,y values into array using numpy
x_array = np.array(x)
y_array = np.array(y)
plt.plot(x_array, y_array)

# Setting font for axis label
font1 = {'family':'serif', 'color':'black', 'size':8}
plt.xlabel("Sieve Sizes (mm)", fontdict=font1)
plt.ylabel("% Passing", fontdict=font1)

# Setting log scale for x-axis and fixing gridlines
plt.xscale('log')
plt.grid(True, color = 'k')

#Evaluating D60, D30 and D10 using interpolation method in scipy
ax = plt.gca()
line = ax.lines[0]
x_data = np.array(line.get_xdata())
y_data = np.array(line.get_ydata())
d_datas = interpolate.interp1d(y_data,x_data, bounds_error= False)
D60 = d_datas([60])
D30 = d_datas([30])
D10 = d_datas([10])

#Check if D10, D30 and D60 have values and setting them to zero
if np.isnan(D10):
	D10 = 0
if np.isnan(D30):
	D30 = 0
if np.isnan(D60):
	D60 = 0

# Evaluating %passing sieve sizes for classification
passing_sieve_5mm = data_value[0]
passing_sieve_2mm = data_value[1]
passing_sieve_425micro_m = data_value[2]
passing_sieve_75micro_m = data_value[3]

# Taking in values for liquid limit and plastic limit
liquid_limit_1 = float(input("Enter Liquid Limit: "))
liquid_limit = int(liquid_limit_1)
plastic_limit_1 = float(input("Enter Plastic Limit: "))
plastic_limit = int(plastic_limit_1)

#Store my Soil Classes in this list
soil_list = []   

# Initializing the varaibles to be stored in the soil_list with NULL
AASHTO_soil_classification = ""
USCS_soil_classification = ""

# CHecking Plastic limit
if plastic_limit > 0:
	PI = liquid_limit - plastic_limit
else:
	PI = 0

# Conditional Statements to Classify AASHTO
if passing_sieve_2mm <= 50 and passing_sieve_425micro_m <= 30 and passing_sieve_75micro_m <= 15 and PI <= 6:
    AASHTO_soil_classification = AASHTO[0][0]
elif passing_sieve_425micro_m <= 50 and passing_sieve_75micro_m <= 25 and PI <= 6:
    AASHTO_soil_classification = AASHTO[0][1]
elif passing_sieve_75micro_m <= 10 and PI == 0:
    AASHTO_soil_classification = AASHTO[1]
elif passing_sieve_75micro_m <= 35 and liquid_limit <= 40 and PI <= 10:
    AASHTO_soil_classification = AASHTO[2][0]
elif passing_sieve_75micro_m <= 35 and liquid_limit >= 41 and PI <= 10:
    AASHTO_soil_classification = AASHTO[2][1]
elif passing_sieve_75micro_m <= 35 and liquid_limit <= 40 and PI >= 11:
    AASHTO_soil_classification = AASHTO[2][2]
elif passing_sieve_75micro_m <= 35 and liquid_limit >= 41 and PI >= 11:
    AASHTO_soil_classification = AASHTO[2][3]
elif liquid_limit <= 40 and PI <= 10:
    AASHTO_soil_classification = AASHTO[3]
elif liquid_limit >= 41 and PI <= 10:
    AASHTO_soil_classification = AASHTO[4]
elif liquid_limit <= 40 and PI >= 11:
    AASHTO_soil_classification = AASHTO[5]
elif liquid_limit >= 41 and PI >= 11 and plastic_limit > 30:
    AASHTO_soil_classification = AASHTO[6][0]
elif liquid_limit >= 41 and PI >= 11 and plastic_limit < 30:
    AASHTO_soil_classification = AASHTO[6][1]
else: pass

#Store AASHTO Classification for Soil Report in soil_list
soil_list.append(AASHTO_soil_classification)

#Cheking for D10
if D10 <= 0:
    Coeff_of_Curvature = 0
    Coeff_of_Uniformity = 0
else:
    Coeff_of_Uniformity = D60/D10
    Coeff_of_Curvature = (D30**2)/(D60*D10)

#Check the A-Line plot for USCS Classification
graph_check = (PI+14.6)/liquid_limit

# Conditional Statements to Classify USCS
if passing_sieve_75micro_m < 50:
    if passing_sieve_5mm < 50:
        if passing_sieve_75micro_m < 5:
            if Coeff_of_Uniformity > 4 and Coeff_of_Curvature >= 1 and Coeff_of_Curvature <= 3:
                USCS_soil_classification = USCS[0][0]
            else:
                USCS_soil_classification = USCS[0][1]
                
        elif passing_sieve_75micro_m > 12:
            if graph_check < 0.73 or PI < 4:
                USCS_soil_classification = USCS[0][2]
            elif graph_check > 0.73 and PI > 7:
                USCS_soil_classification = USCS[0][3]
            else:
                USCS_soil_classification = USCS[0][2],"-",USCS[0][3]
            
        elif passing_sieve_75micro_m >= 5 and passing_sieve_75micro_m <= 12:
            USCS_soil_classification = USCS[0][0],"-",USCS[0][2]

    else:
        if passing_sieve_75micro_m < 5:
            if Coeff_of_Uniformity > 6 and Coeff_of_Curvature >= 1 and Coeff_of_Curvature <= 3:
                USCS_soil_classification = USCS[1][0]
            else:
                USCS_soil_classification = USCS[1][1]

        elif passing_sieve_75micro_m > 12:
            if graph_check < 0.73 or PI < 4:
                USCS_soil_classification = USCS[1][2]
            elif graph_check > 0.73 and PI > 7:
                USCS_soil_classification = USCS[1][3]
            else:
                USCS_soil_classification = USCS[1][2],"-",USCS[1][3]
        elif passing_sieve_75micro_m >= 5 and passing_sieve_75micro_m <= 12:
            USCS_soil_classification = USCS[1][1],"-",USCS[1][3]

else:
    if liquid_limit <= 50:
        if graph_check > 0.73:
            USCS_soil_classification = USCS[2][0]
        else:
            USCS_soil_classification = USCS[2][1]
    elif liquid_limit > 50:
        if graph_check > 0.73:
            USCS_soil_classification = USCS[3][0]
        else:
            USCS_soil_classification = USCS[3][1]

#Store USCS classification for Soil Report in soil_list
soil_list.append(USCS_soil_classification)      

#Save the graph
plt.savefig(new_path+"/out_put_graph.png", bbox_inches= "tight", dpi = 95)

#Importing Module to Present Result into pdf format
from reportlab.pdfgen import canvas
from reportlab.lib import colors

#String Format for PdF Presentation
Heading = "SOIL CLASSIFICATION REPORT"
date_heading = str(datetime.datetime.today())
Atterberg =  "Plastic Limit = {}%    Liquid Limit = {}%".format((plastic_limit_1), (liquid_limit_1))
finess_mod = "Fineness Modulus = {}".format(finess_modulus)

# Cater for when D30 or D10 are not defined
try:
    D_list = "D60 = {} mm    D30 = {} mm     D10 = {} mm".format(round(D60[0],2), round(D30[0],2), round(D10[0],2))
    Coeff1 = "Coefficient of Uniformity = {}".format(round(Coeff_of_Uniformity[0],2))
    Coeff2 = "Coefficient of Curvature = {}".format(round(Coeff_of_Curvature[0],2))

except TypeError:
        try: 
            D_list = "D60 = {} mm    D30 = {} mm".format(round(D60[0],2), round(D30[0],2))
        except TypeError:
            try:
                D_list = "D60 = {} mm".format(round(D60[0],2))
            except TypeError:
                pass

# Entering path to save result   
file_path_1 = (input('Enter the file path to save PDF report            '))
file_name_1, file_extension_1 = os.path.splitext(file_path_1)

# Checking the file extension to make sure code doesn't break 
while file_extension_1 not in [".pdf"]:
    print("FileExtensionError. File extension should be: \".pdf\" such as file_name.pdf")
    file_path_1 = (input('Enter the file path to save PDF report            '))
    file_name_1, file_extension_1 = os.path.splitext(file_path_1)

# Continue here when above is passed
fileName = file_path_1

# This is a function to place coordinates on my pdf sheet. But first Remove Comment if you wish to use it
'''def drawMyRuler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')'''

#Create and Save pdf file
pdf = canvas.Canvas(fileName)

# Use this to set text and image on pdf file but first remove commnents if you wish to use it
'''drawMyRuler(pdf)'''    

#Title for pdf
pdf.setTitle("Soil Report")

#Heading
pdf.setFont("Times-Roman", 16)
pdf.setFillColor(colors.blue)
pdf.drawCentredString(270, 780, Heading)

# Date 
pdf.setFont("Times-Roman", 10)
pdf.setFillColor(colors.red)
pdf.drawString(400, 780, date_heading)

# Heading for graph
pdf.setFont("Courier", 13)
pdf.setFillColor(colors.black)
pdf.drawString(270, 750, "Sieve Analysis")

# Inserting graph
pdf.drawInlineImage(new_path+"/out_put_graph.png", 25, 330)

# Cater for when Coefficient of Curvature or Uniformity are not defined
try:
        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.black)
        pdf.drawString(100, 300, D_list)

        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.black)
        pdf.drawString(100, 270, finess_mod)

        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.black)
        pdf.drawString(100, 240, Atterberg)

        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.black)
        pdf.drawString(100, 210, Coeff1)

        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.black)
        pdf.drawString(100, 180, Coeff2)

        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.red)
        pdf.drawString(100, 150, soil_list[0])

        pdf.setFont("Times-Roman", 15)
        pdf.setFillColor(colors.blue)
        if soil_list[1] == USCS[2][1] or soil_list[1] == USCS[3][1]:
            text = soil_list[1].split("\n")
            pdf.drawString(100, 120, text[0])
            pdf.drawString(100, 100, text[1])
        else:
            pdf.drawString(100, 120, soil_list[1])

except NameError:
        try:
            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.black)
            pdf.drawString(100, 300, D_list)

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.black)
            pdf.drawString(100, 270, finess_mod)

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.black)
            pdf.drawString(100, 240, Atterberg)

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.red)
            pdf.drawString(100, 210, soil_list[0])

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.blue)
            if soil_list[1] == USCS[2][1] or soil_list[1] == USCS[3][1]:
                text = soil_list[1].split("\n")
                pdf.drawString(100, 180, text[0])
                pdf.drawString(100, 160, text[1])
            else:
                pdf.drawString(100, 180, soil_list[1])

        except NameError:
            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.black)
            pdf.drawString(100, 300, finess_mod)

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.black)
            pdf.drawString(100, 270, Atterberg)
            
            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.red)
            pdf.drawString(100, 240, soil_list[0])

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.blue)
            if soil_list[1] == USCS[2][1] or soil_list[1] == USCS[3][1]:
                text = soil_list[1].split("\n")
                pdf.drawString(100, 210, text[0])
                pdf.drawString(100, 190, text[1])
            else:
                pdf.drawString(100, 210, soil_list[1])

    # Saving the Report and Catering for scenario when error pops up.
try:
        pdf.save()
except PermissionError:
    print("Please close the current file in your pdf viewer if opened and rerun the program")