import pandas as pd

def finess_modulus(file_path):
    #file = open(file_path, newline='')
    file = pd.read_csv(file_path)
    my_list = []

    for row in file.values:
        my_list.append(list(row))

    #Store Sieve Sizes and %Passing for all Sieves
    data = []     
    for row in my_list:
        #sieve_size, wt of sieve, wt of sieve+sample, wt retained, %retained, cumm. retained, %passing
        sieve_size = float(row[0])
        cumm_ret = float(row[-2])
        data.append((sieve_size, cumm_ret))
    
    #Storing %cumm_retained for sieve sizes: 5mm, 2.36mm, 1.18mm, 0.6mm, 0.3mm and 0.15mm
    
    data_value_ret = []      
    for row in data:
        if row[0] in [5, 4.75, 2.36, 1.18, 0.6, 0.3, 0.15]:
            data_value_ret.append(row[-2])

    sum = 0
    for i in range(0,len(data_value_ret)):
        sum += data_value_ret[i]

    finess_mod = round(sum/100,2)

    return(finess_mod)