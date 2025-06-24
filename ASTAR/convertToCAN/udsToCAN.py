import json
import pandas as pd
import os
from pathlib import Path
# Sample UDS JSON content (you can replace this with full JSON loading from file)
uds_json = {
    "current": {
        "equation": "((signed(A)*256)+B)*0.1",
        "minValue": "-500",
        "maxValue": "300",
        "type": "Number",
        "command": "2248F9",
        "ecu": "7E4"
    },
    "voltage": {
        "equation": "((A<<8)+B)*0.01",
        "minValue": "300",
        "maxValue": "500",
        "type": "Number",
        "command": "22480D",
        "ecu": "7E4"
    },
    "soc": {
        "equation": "A*0.5",
        "minValue": "-5",
        "maxValue": "105",
        "type": "Number",
        "command": "224845",
        "ecu": "7E4"
    }
}

#import file
car = 'FordMustangMachE'
folder_path = 'C:/Users/Zu Kai/ASTAR/output_csvs/'
path = f'convertToCAN/UDSjson/{car}.json'
uds_json_full = json.load(open(path, 'r'))
# print(uds_json_full)


# Generate CAN frame data
can_frames = []
parameters = ['init_commands', 'obd_protocol', 'data_commands']
for param_name, details in uds_json_full.items():
    if param_name in parameters:
        continue
    else:
        command_hex = details["command"]
        can_id = int(details["ecu"], 16)
        # Convert command string to byte list
        data_bytes = [int(command_hex[i:i+2], 16) for i in range(0, len(command_hex), 2)]
        data_bytes += [0x00] * (8 - len(data_bytes))  # Pad to 8 bytes
        can_frames.append({
            "Parameter": param_name,
            "CAN_ID": hex(can_id),
            "DLC": len(data_bytes),
            "Data": ' '.join(f'{byte:02X}' for byte in data_bytes),
            "Message to send": '0'+ str(len(data_bytes)) + ' ' + ' '.join(f'{byte:02X}' for byte in data_bytes)
        })

# Create DataFrame for display
df_can_frames = pd.DataFrame(can_frames)
print(df_can_frames)

# # Output CSV name
base_filename = Path(path).stem
# print(base_filename)

# Create output directory
output_dir = Path("CAN msgs to send")
output_dir.mkdir(exist_ok=True)

# Construct full output path: output/myfile.csv
csv_path = output_dir / f"{base_filename}.csv"

# Output CSV
df_can_frames.to_csv(csv_path, index=False)