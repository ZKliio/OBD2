import os
import csv

# 🔧 Replace this with your actual directory path
root_dir = "./output_parameters_DID"
# Dictionary to store file path and row count
csv_row_counts = {}

# Walk through all subdirectories and files
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.lower().endswith(".csv"):
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    row_count = sum(1 for row in reader)
                    csv_row_counts[file_path] = row_count
            except Exception as e:
                csv_row_counts[file_path] = f"Error reading file: {e}"

# Print the results
for path, count in csv_row_counts.items():
    print(f"{path}: {count} rows")

print(f"Total rows: {sum(csv_row_counts.values())}")
