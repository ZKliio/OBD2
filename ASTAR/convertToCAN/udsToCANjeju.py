# 

import pandas as pd
import os

folder_path = 'C:/Users/Zu Kai/ASTAR/output_csvs/'
files = os.listdir(folder_path) #create a list of files in the folder
#import file
import csv

model = 'KIA'
car = 'Optima_PHEV'
path = f'BMS_CSVs/{model}/{car}_BMS_data.csv'

with open(path, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)  # each row is a dictionary

# print(data[0:4])  # example: print first row


# Parse the rows into a list of dicts
records = []
for parts in data:
    if len(parts) >= 4:
        param_name = parts[0]
        short_name = parts[1]
        # Extract DID
        if len(parts[2]) == 6:
            did = str(parts[2])[2:]
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
            "UDS Request Payload": data
        })

# Create DataFrame
df = pd.DataFrame(records)

print(df)

# Output to CSV in a specific folder
output_folder = "output_csvs"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, f"{car}.csv")
df.to_csv(output_file, index=False)

df.head()
