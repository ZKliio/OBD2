import cantools
import random


db = cantools.database.load_file('convertToCAN/cars/toyota_prius_2010_pt.dbc')

for message in db.messages:
    # Auto-generate dummy values (0.0 for now)
    values = {signal.name: 0.0 for signal in message.signals}
    
    # values = {signal.name: random.uniform(signal.minimum, signal.maximum) for signal in message.signals}
    
    try:
        encoded = message.encode(values)
        print(f"Message: {message.name} (0x{message.frame_id:X})")
        print(f"Encoded: {encoded.hex()}")
        print()
    except Exception as e:
        print(f"Failed to encode {message.name}: {e}")

# import csv
# import cantools
# import random
# from collections import defaultdict

# # Load DBC
# db = cantools.database.load_file('dbcFileConvert/cars/toyota_prius_2010_pt.dbc')

# # Load CSV and group signals by message
# msg_signals = defaultdict(list)

# with open('test.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         msg_name = row['Message_Name']
#         signal_name = row['Signal_Name (DID)']
#         msg_signals[msg_name].append(signal_name)

# # Encode each message
# for msg_name, signal_list in msg_signals.items():
#     try:
#         msg = db.get_message_by_name(msg_name)
#         values = {}

#         for signal in msg.signals:
#             if signal.name in signal_list:
#                 # Assign random valid value within min/max
#                 min_val = signal.minimum if signal.minimum is not None else 0
#                 max_val = signal.maximum if signal.maximum is not None else 100
#                 values[signal.name] = round(random.uniform(min_val, max_val), 2)

#         encoded = msg.encode(values)
#         print(f"{msg_name} (0x{msg.frame_id:X}): {encoded.hex()}  ← {values}")
#     except Exception as e:
#         print(f"Failed to encode {msg_name}: {e}")
