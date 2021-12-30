import pandas as pd
import glob
import os 
from pathlib import Path
filepaths = [f for f in os.listdir(".") if f.endswith('.csv')]


def concat_data():

    dir_path=r'E:\New folder\Udemy\personal data science projects\book reviews analysis\english\politics\data'

    #get all the csv files 
    filepaths = [f for f in os.listdir(dir_path) if f.endswith('.csv')]

    #sort the files
    #using .sort() doesnt sort ascendingly
    sorted_files = sorted(filepaths, key=lambda x: int(x.split('_')[0]))
    #print(sorted_files)


    clean_files=[]
    for file in sorted_files:
        current_file=(dir_path + '\\' + file)
        clean_files.append(current_file)
    
    #print(clean_files)

    df = pd.concat(map(pd.read_csv, clean_files), ignore_index=True)
    df.to_csv(r'E:\New folder\Udemy\personal data science projects\book reviews analysis\english\politics\df.csv')

concat_data()

