import pandas as pd

def sieve_data(file_path):
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
        passing = round(float(row[-1]), 3)
        data.append((sieve_size, passing))

        #Storing %passing for sieve sizes: 5mm, 2mm, 0.425 and 0.075
    data_value = []      
    for row in data:
        if row[0] in [5, 4.75, 2, 0.425, 0.075]:
            data_value.append(row[-1])
    return(data_value)