import json
import pandas as pd
import os


def safe_hex_to_int(value):
    try:
        return int(value, 16)
    except (ValueError, TypeError):
        return None
def byte_length_check(command_hex):
    if len(command_hex) == 6:
        print(command_hex)
        # print([int(command_hex[i:i+2], 16) for i in range(0, len(command_hex), 2)])
        return [int(command_hex[i:i+2], 16) for i in range(0, len(command_hex), 2)]
    else:
        command_hex = command_hex[2:8]
        # print([int(command_hex[i:i+2], 16) for i in range(0, len(command_hex), 2)])
        return [int(command_hex[i:i+2], 16) for i in range(0, len(command_hex), 2)]
    
    pass

#import file
def main(mock_input, sourcelink):
    folder_path = r'C:/Users/Zu Kai/astar_git/OBD2/ev-obd-pids'
    files = os.listdir(folder_path) #create a list of files in the folder

    excluded_files = ["obdble_cars.json", "README.md", "Mini"]
    
    # Filter the list
    files = [file for file in files if file not in excluded_files]

    for index, file in enumerate(files):
        print(f"{index}: {file}")

    manufacturer = files[int(mock_input('Choose Manufacturer by Index: \n'))]
    folder_path = f'{folder_path}/{manufacturer}'

    files = os.listdir(folder_path)

    for index, file in enumerate(files):
        print(f"{index}: {file}")

    model = files[int(mock_input('Choose Model by Index: \n'))]
    path = f'{folder_path}/{model}'
    print(path)

    with open(path, 'r') as f:
        uds_json_full = json.load(f)

    # Generate CAN frame data
    can_frames = []
    parameters = ['init_commands', 'obd_protocol', 'data_commands']
    for param_name, details in uds_json_full.items():
        if param_name in parameters:
            continue
        else:
            command_hex = details["command"]
            can_id = safe_hex_to_int(details["ecu"])
            # Convert command string to byte list
            data_bytes = byte_length_check(command_hex)
            # print([hex(i) for i in data_bytes]) # debug if command_hex received properly (command_hex = SID22/DID)

            data_bytes += [0x00] * (8 - 1 - len(data_bytes))  # Pad to 8 bytes (-1 because 03 is added later)
            can_frames.append({
                "Parameter": param_name,
                "CAN_ID": '%x' % can_id if can_id is not None else None,
                # "DLC": len(data_bytes),
                # "Data": ' '.join(f'{byte:02X}' for byte in data_bytes),
                "UDS Request Payload": '03' + ' ' + ' '.join(f'{byte:02X}' for byte in data_bytes),
                "Vehicle Model": model[:-5],
                "Source": sourcelink

            })

    # Create DataFrame for display
    df_can_frames = pd.DataFrame(can_frames)
    print(df_can_frames)

    # # Output CSV name
    # base_filename = Path(folder_path).stem
    # print(base_filename)

    # Create output directory
    output_dir = f"C:/Users/Zu Kai/astar_git/OBD2/output_parameters_DID/{manufacturer}"
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{model[:-5]}.csv")
    # Construct full output path: output/myfile.csv
    df_can_frames.to_csv(output_file, index=False)

    df_can_frames.head()