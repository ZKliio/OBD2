import csv
import os

folder_path = 'C:/Users/Zu Kai/ASTAR/output_csvs/'
files = os.listdir(folder_path)

for index, file in enumerate(files):
    print(f"{index}: {file}")

filepath = files[int(input('Choose File by Index: \n'))]

param_dict = {}
can_msgs = []
car_brand = 'Hyundai'
car_model = 'Ioniq_EV'

with open(f'C:/Users/Zu Kai/ASTAR/output_csvs/{filepath}', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        param_name = row['Parameter']  # Ensure this matches your CSV header
        param_dict[param_name] = row['UDS Request Payload']  # Entire row as the value
        can_msgs.append(row['UDS Request Payload'])
# Example: Access the DID of a specific parameter
# print(param_dict['000_Battery DC Voltage']['DID'])  # Replace with actual parameter name

# for item in param_dict.items():
#     print(f'{item}\n')

# print(can_msgs)
iternary = [print(f'{key[4:]}') for key in param_dict.keys()]
# print(param_dict.keys())
# for i in param_dict.keys():
query_name = input('Choose which parameter you want to query:\n')
payload = param_dict[f'000_{query_name}']
byte_list = [int(b, 16) for b in payload.strip().split()]
print(byte_list)
