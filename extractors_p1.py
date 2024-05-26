import os
import csv
import sys

# Function to parse a single file
def parse_file(input_file):
    with open(input_file, 'r', encoding="ISO-8859-1") as file:
        lines = file.readlines()

    # Initialize variables to store extracted data
    angle = None
    correlation_data = []

    # Flag to determine when to start collecting correlation data
    start_collecting_correlation = False

    # Iterate through each line in the file
    for line in lines:
        parts = line.strip().split(':')
        
        # Extract angle from the first line
        if "Angle" in parts[0]:
            angle = parts[1].strip()

        # Start collecting correlation data after encountering the "Correlation" line
        if "Correlation" in line:
            start_collecting_correlation = True
            continue

        # Stop collecting data after encountering the "Count Rate" line
        if "Count Rate" in line:
            break

        # If collecting correlation data, extract the first two columns
        if start_collecting_correlation:
            data_points = line.strip().split()
            if len(data_points) >= 2:  # Check if there are at least two elements in data_points
                correlation_data.append([data_points[0], data_points[1]])

    return angle, correlation_data

# Function to write extracted data to a CSV file
def write_to_csv(output_file, angle, correlation_data):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([angle])  # Writing angle row with empty cells
        writer.writerows(correlation_data)

# Input and output directories
input_dir = "ALV_FILES" # Input directory from the first command line argument
output_dir = "g2-1_files" # Output directory from the second command line argument

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each ASC file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.ASC'):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename[:-4] + '_g2-1.csv')

        # Parse the file
        angle, correlation_data = parse_file(input_file)

        # Write extracted data to CSV
        write_to_csv(output_file, angle, correlation_data)

