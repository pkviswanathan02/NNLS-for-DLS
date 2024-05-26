import os
import csv
import math

# Function to calculate y2
def calculate_y2(y1):
    y1_float = float(y1)
    y1_abs = abs(y1_float)
    return math.sqrt(y1_abs) * (y1_abs / y1_float)

# Input and output directories
input_dir = 'g2-1_files'
#output_dir = os.path.join(input_dir, 'g1')
output_dir = 'g1'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process each CSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename.replace('_g2-1.csv', '_g1.txt'))

        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Extract angle from the first line
        angle = float(lines[0].strip())

        # Calculate y2 and write to the output file
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ')

            for line in lines[1:]:
                x, y1 = line.strip().split(',')
                y2 = calculate_y2(float(y1))
                writer.writerow([angle, x, y2])

print("Conversion complete.")
