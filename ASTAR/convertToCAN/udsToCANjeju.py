################# Source #######################
# https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master


import pandas as pd
import os
import csv


def main(mock_input, sourcelink):
    folder_path = r'C:/Users/Zu Kai/astar_git/OBD2/ASTAR/BMS_CSVs/'
    files = os.listdir(folder_path) #create a list of files in the folder

    for index, file in enumerate(files):
        print(f"{index}: {file}")
    manufacturer = files[int(mock_input('Choose Manufacturer by Index: \n'))]
    folder_path = f'{folder_path}/{manufacturer}'
    
    files = os.listdir(folder_path)
    for index, file in enumerate(files):
        print(f"{index}: {file}")
    model = files[int(mock_input('Choose Model by Index: \n'))]

    path = f'{folder_path}/{model}'

    with open(path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)  # each row is a dictionary

    # print(data[0:4])  # example: print first row


    # Parse the rows into a list of dicts
    records = []
    for parts in data:
        if len(parts) >= 4: # dont really need this its redundant
            param_name = parts[0]
            short_name = parts[1]
            print(param_name, short_name)
            # Extract DID
            if len(parts[2]) > 6:
                did_extended = parts[2]
                did = did_extended[4:]
                # print(did)
            elif len(parts[2]) == 6:
                did_extended = parts[2]
                did = (did_extended[2:])
                # print(did)
            elif len(parts[2]) == 4: 
                did = parts[2]
            
            else:
                print('INVALID DID', parts[2])
                did = '0x0000'
                continue
            ecu = parts[-1]
            # Ensure DID is hexadecimal with 0x prefix
            did_hex = f"0x{did.lower()}" if not did.startswith("0x") else did.lower()
            # SID 0x22 for UDS ReadDataByIdentifier
            data = f"03 22 {did[0:2]} {did[2:]}"
            # print(''.join(data.split()))  # debug CAN msg output (UDS request payload 22 21...)
            for i in range(8 - (len(''.join(data.split()))//2)):
                data += ' 00'

            records.append({
                "Parameter": param_name,
                "Short Name": short_name,
                "CAN ID": ecu,
                "DID": did_hex,
                "UDS Request Payload": data,
                "Vehicle": model[:-9],
                "source": {sourcelink}
            })

    # Create DataFrame
    df = pd.DataFrame(records)

    print(df)

    # Output to CSV in a specific folder
    output_folder = f"output_parameter_DID/{manufacturer}"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{model}")
    df.to_csv(output_file, index=False)

    df.head()
