import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import numpy as np
from scipy import interpolate
import os

def alter_graph(*my_list):

    plt.plot([5.00, 2.00, 0.425, 0.075], [y for y in my_list])

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
        D10 = [0.0]
    if np.isnan(D30):
        D30 = [0.0]
    if np.isnan(D60):
        D60 = [0.0]

    #Cheking for D10
    if D10[0] <= 0:
        Coeff_of_Curvature = [0.0]
        Coeff_of_Uniformity = [0.0]
    else:
        Coeff_of_Uniformity = D60/D10
        #Coeff_of_Uniformity = np.round(Coeff_of_Uniformity, 3)
        Coeff_of_Curvature = (D30**2)/(D60*D10)
        #Coeff_of_Curvature = np.round(Coeff_of_Curvature, 3)

    '''D60 = np.round(d_datas([60]), 2)
    D30 = np.round(d_datas([30]), 2)
    D10 = np.round(d_datas([10]), 2)
    
    list_D_Cu_CC = []
    list_D_Cu_CC.append(D60)
    list_D_Cu_CC.append(D30)
    list_D_Cu_CC.append(D10)
    list_D_Cu_CC.append(Coeff_of_Uniformity)
    list_D_Cu_CC.append(Coeff_of_Curvature)'''

    new_path = (os.path.dirname(__file__)).replace("\\","/")

    plt.savefig(new_path+"/static/out_put_graph.png", bbox_inches= "tight", dpi = 95)
    plt.clf()

    return D60[0], D30[0], D10[0], Coeff_of_Uniformity[0], Coeff_of_Curvature[0]