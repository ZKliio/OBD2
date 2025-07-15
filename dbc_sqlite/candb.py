import sqlite3
import re
import os

conn = sqlite3.connect("can.db")
cursor = conn.cursor()

# Create tables from schema.sql
with open(r"C:/Users/Zu Kai/astar_git/OBD2/dbc_sqlite/schema.sql", encoding="utf-8") as f:
    cursor.executescript(f.read())

def main(filename, car_model, variant):
    with open(rf"C:/Users/Zu Kai/astar_git/OBD2/dbc/{filename}", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Insert or get car_model
    cursor.execute("INSERT OR IGNORE INTO car_models (name) VALUES (?)", (car_model,))
    cursor.execute("SELECT id FROM car_models WHERE name = ?", (car_model,))
    car_model_id = cursor.fetchone()[0]

    # Insert dbc_file
    cursor.execute("""
        INSERT INTO dbc_files (name, car_model_id, variant) VALUES (?, ?, ?)
    """, (filename, car_model_id, variant))

    # Get dbc_file_id to associate messages/signals
    cursor.execute("SELECT id FROM dbc_files WHERE name = ?", (filename,))
    dbc_file_id = cursor.fetchone()[0]

    msg_db_id = None
    for line in lines:
        if line.startswith("BO_ "):
            parts = line.split()
            message_id = int(parts[1])
            name = parts[2].rstrip(':')
            dlc = int(parts[3])
            sender = parts[4]
            cursor.execute("""
                INSERT INTO messages (message_id, name, dlc, sender, car_model_id, dbc_id)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (message_id, name, dlc, sender, car_model_id, dbc_file_id))
            msg_db_id = cursor.lastrowid

        elif line.startswith("SG_ ") and msg_db_id is not None:
            sig_match = re.match(r"SG_\s+(\w+)\s*:\s*(\d+)\|(\d+)@(\d)([+-])\s+\(([^,]+),([^)]+)\)\s+\[([^|]+)\|([^\]]+)\]\s+\"([^\"]*)\"\s+(\w+)", line)
            if sig_match:
                sig_name, start, length, byte_order, sign, factor, offset, min_val, max_val, unit, receiver = sig_match.groups()
                cursor.execute("""
                    INSERT INTO signals 
                    (message_id, name, start_bit, length, byte_order, is_signed, factor, offset, min, max, unit, receiver)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (msg_db_id, sig_name, int(start), int(length),
                     'motorola' if byte_order == '0' else 'intel',
                     1 if sign == '-' else 0, float(factor), float(offset),
                     float(min_val), float(max_val), unit, receiver))

        elif line.startswith("BO_TX_BU_"):
            match = re.match(r"BO_TX_BU_\s+(\d+)\s+:\s+(.+);", line)
            if match:
                mid = int(match.group(1))
                transmitters = [t.strip() for t in match.group(2).split(',')]
                for t in transmitters:
                    cursor.execute("INSERT INTO transmitters (message_id, transmitter) VALUES (?, ?)", (mid, t))

        elif line.startswith("CM_ SG_"):
            match = re.match(r'CM_ SG_ (\d+)\s+(\w+)\s+\"(.+)\";', line)
            if match:
                mid, sig_name, comment = match.groups()
                cursor.execute("INSERT INTO signal_comments (message_id, signal_name, comment) VALUES (?, ?, ?)",
                               (int(mid), sig_name, comment))

        elif line.startswith("VAL_"):
            match = re.match(r"VAL_ (\d+)\s+(\w+)\s+(.+);", line)
            if match:
                mid, sig_name, mappings = match.groups()
                value_pairs = re.findall(r'(\d+)\s+\"([^\"]+)\"', mappings)
                for val, meaning in value_pairs:
                    cursor.execute("INSERT INTO signal_values (message_id, signal_name, value, meaning) VALUES (?, ?, ?, ?)",
                                   (int(mid), sig_name, int(val), meaning))

# Run for two DBCs
for file in ["acura_ilx_2016_nidec.dbc", "acura_ilx_2016_can_generated.dbc", "bmw_e9x_e8x.dbc"]: #"bmw_e9x_e8x.dbc"
    car_model = "_".join(file.split("_")[:3])
    variant = file.replace(car_model, "").strip("_").replace(".dbc", "") or None
    print(f"Inserting {file} ({car_model}, {variant})...")
    main(file, car_model, variant)

conn.commit()
conn.close()
print("All Done!")