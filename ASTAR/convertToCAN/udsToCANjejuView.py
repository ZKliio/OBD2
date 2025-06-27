################# Source #######################
# https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master


import pandas as pd
import os
import csv


view = input('View original file: 0\nView parsed file: 1\n')

while view not in ['0', '1']:
    print('Invalid input. Please enter 0 or 1.')
    view = input('View original file: 0\nView parsed file: 1\n')

if view == '0':
    folder_path = r'C:/Users/Zu Kai/astar_git/OBD2/ASTAR/BMS_CSVs/'
    files = os.listdir(folder_path) #create a list of files in the folder
    for index, file in enumerate(files):
        print(f"{index}: {file}")
    manufacturer = files[int(input('Choose Manufacturer by Index: \n'))]
    folder_path = f'{folder_path}/{manufacturer}'
    files = os.listdir(folder_path)
    for index, file in enumerate(files):
        print(f"{index}: {file}")
    model = files[int(input('Choose Model by Index: \n'))]
    path = f'{folder_path}/{model}'
    df = pd.read_csv(f"{path}", dtype=str)
    print(df)

elif view == '1':
    folder_path = r'C:/Users/Zu Kai/astar_git/OBD2/ASTAR/convertToCAN/output_parameter_DID'
    files = os.listdir(folder_path) #create a list of files in the folder
    for index, file in enumerate(files):
        print(f"{index}: {file}")
    manufacturer = files[int(input('Choose Manufacturer by Index: \n'))]
    folder_path = f'{folder_path}/{manufacturer}'
    files = os.listdir(folder_path)
    for index, file in enumerate(files):
        print(f"{index}: {file}")
    model = files[int(input('Choose Model by Index: \n'))]
    path = f'{folder_path}/{model}'
    df = pd.read_csv(f"{path}", dtype=str)
    print(df)

        

