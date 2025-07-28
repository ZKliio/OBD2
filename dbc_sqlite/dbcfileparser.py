import os
folder_path = r'C:/Users/Zu Kai/astar_git/OBD2/dbc'
files = os.listdir(folder_path)
dbc_files = [file for file in files if file.lower().endswith('.dbc')]

dict = {}
for file in (dbc_files):
    # print(f'Filename: {file}')
    # car_model = "_".join(file.split("_")[:3])
    split = (file.split("_"))
    print(split)
    manufacturer = split[0]
    if len(split) >= 4:
        model = split[1] + "_" + split[2]
        dict[manufacturer] = dict.get(manufacturer, []) + [file]