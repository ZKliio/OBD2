# import cantools

# db = cantools.database.load_file("dbcFileConvert/cars/toyota_prius_2010_pt.dbc")
# msg = db.get_message_by_name('KINEMATICS')

# # List all signal names
# signal_names = [signal.name for signal in msg.signals]
# print(signal_names)

# print(db.messages)
# # List all signal values
# print(signal for signal in msg.signals)

import os
import cantools
import csv

# Load your DBC file
filename = 'dbcFileConvert/cars/toyota_prius_2010_pt.dbc'
db = cantools.database.load_file(filename)

# Output CSV name
filename = os.path.basename(filename).replace('.dbc', '.csv')

# Output CSV
with open('can_signals.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Message_Name', 'Message_ID (PID)', 'Signal_Name (DID)'])

    for message in db.messages:
        for signal in message.signals:
            writer.writerow([
                message.name,
                hex(message.frame_id),  # PID
                signal.name             # DID
            ])
