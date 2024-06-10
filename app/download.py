import os
#import MySQLdb
#Importing Module to Present Result into pdf format
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import datetime

def download_pdf(plastic_limit_1, liquid_limit_1, fines_modulus, D60, D30, D10, C_of_U, C_of_C, aashto_class, uscs_class):

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

    #Get path to python file,
    new_path = (os.path.dirname(__file__)).replace("\\","/")

    #String Format for PdF Presentation
    Heading = "SOIL CLASSIFICATION REPORT"
    date_heading = str(datetime.datetime.today())
    Atterberg =  "Plastic Limit = {}%    Liquid Limit = {}%".format((plastic_limit_1), (liquid_limit_1))
    finess_mod = "Fineness Modulus = {}".format(fines_modulus)

    # Cater for when D30 or D10 are not defined
    try:
        D_list = "D60 = {} mm    D30 = {} mm     D10 = {} mm".format(round(D60,2), round(D30,2), round(D10,2))
        Coeff1 = "Coefficient of Uniformity = {}".format(round(C_of_U,2))
        Coeff2 = "Coefficient of Curvature = {}".format(round(C_of_C,2))

    except TypeError:
            try: 
                D_list = "D60 = {} mm    D30 = {} mm".format(round(D60,2), round(D30,2))
            except TypeError:
                try:
                    D_list = "D60 = {} mm".format(round(D60,2))
                except TypeError:
                    pass

    # Entering path to save result   

    new_path = (os.path.dirname(__file__)).replace("\\","/")

    fileName = new_path+"/static/soil_report.pdf"

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
    pdf.drawInlineImage(new_path+"/static/out_put_graph.png", 25, 330)

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
            pdf.drawString(100, 150, aashto_class)

            pdf.setFont("Times-Roman", 15)
            pdf.setFillColor(colors.blue)
            if uscs_class == USCS[2][1] or uscs_class == USCS[3][1]:
                text = uscs_class.split("\n")
                pdf.drawString(100, 120, text[0])
                pdf.drawString(100, 100, text[1])
            else:
                pdf.drawString(100, 120, uscs_class)

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
                pdf.drawString(100, 210, aashto_class)

                pdf.setFont("Times-Roman", 15)
                pdf.setFillColor(colors.blue)
                if uscs_class == USCS[2][1] or uscs_class == USCS[3][1]:
                    text = uscs_class.split("\n")
                    pdf.drawString(100, 180, text[0])
                    pdf.drawString(100, 160, text[1])
                else:
                    pdf.drawString(100, 180, uscs_class)

            except NameError:
                pdf.setFont("Times-Roman", 15)
                pdf.setFillColor(colors.black)
                pdf.drawString(100, 300, finess_mod)

                pdf.setFont("Times-Roman", 15)
                pdf.setFillColor(colors.black)
                pdf.drawString(100, 270, Atterberg)
                
                pdf.setFont("Times-Roman", 15)
                pdf.setFillColor(colors.red)
                pdf.drawString(100, 240, aashto_class)

                pdf.setFont("Times-Roman", 15)
                pdf.setFillColor(colors.blue)
                if uscs_class == USCS[2][1] or uscs_class == USCS[3][1]:
                    text = uscs_class.split("\n")
                    pdf.drawString(100, 210, text[0])
                    pdf.drawString(100, 190, text[1])
                else:
                    pdf.drawString(100, 210, uscs_class)

        # Saving the Report and Catering for scenario when error pops up.
    try:
            pdf.save()
    except PermissionError:
        print("Please close the current file in your pdf viewer if opened and rerun the program")

    return fileName