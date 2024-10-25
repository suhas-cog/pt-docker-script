import os
import json
import csv
import zipfile
import sys

replace_files = {
    "transaction" : "Label",
    "sampleCount" : "# Samples",
    "errorCount" : "errorCount",
    "errorPct" : "Error %",
    "meanResTime" : "Average", 
    "minResTime" : "Min",
    "maxResTime" : "Max",
    "pct1ResTime" : "90% Line",
    "pct2ResTime" : "95% Line",
    "pct3ResTime" : "99% Line",
    "throughput" : "throughput",
    "receivedKBytesPerSec" : "receivedKBytesPerSec",
    "sentKBytesPerSec" : "sentKBytesPerSec"
}

# Get the ZIP file path from command-line arguments
if len(sys.argv) != 2:
    raise ValueError("Usage: python python.py home/runner/work/pt-docker-script/pt-docker-script/test_report")

zip_file_path = home/runner/work/pt-docker-script/pt-docker-script/test_report

#if not os.path.isfile(zip_file_path):
#    raise FileNotFoundError(f"No ZIP file found at the specified path: {zip_file_path}")

# Define the extraction directory
extraction_dir = os.path.dirname(os.path.abspath(__file__))

# Extract all files in the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_dir)

# Search for statistics.json in the extracted files
for root, dirs, files in os.walk(extraction_dir):
    if 'statistics.json' in files:
        statistics_json_path = os.path.join(root, 'statistics.json')
        break
else:
    print("statistics.json not found in any subfolder.")

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the path to the JSON file
json_file_path = statistics_json_path

file_name = os.path.basename(zip_file_path).replace('_HTMLReport.zip','')

# Define the path to the CSV file
csv_file_path = os.path.join(current_dir, f'{file_name}.csv')

# Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header
    header_written = False

    for key, value in data.items():
        if not header_written:
            header = list(value.keys())
            csv_writer.writerow(header)
            header_written = True

        row = list(value.values())
        csv_writer.writerow(row)

# Read the CSV file and store its contents
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

    # Find the row with 'Total' in the first column
    total_row = None
    for i, row in enumerate(rows):
        if row[0] == 'Total':
            total_row = rows.pop(i)
            break

    # Append the 'Total' row at the end if it was found
    if total_row:
        rows.append(total_row)

    # Write the updated rows back to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(rows)

# Replace header data values with replace_files key value pair
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)        

# Replace header values
header = rows[0]
new_header = [replace_files.get(col, col) for col in header]
rows[0] = new_header

# Write the updated rows back to the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(rows)
