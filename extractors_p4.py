import csv
from collections import defaultdict
from math import pi, sin, radians, sqrt
import matplotlib.pyplot as plt

# Load Experiment Parameters
with open('ep.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        n = float(row[0])
        λ = float(row[1])
        η = float(row[2])  # Viscosity (Pa.s)
        T = float(row[3])  # Temperature (K)

# Dictionary to store sum of 1000/c and 1000/e values, count, and squared sum for each angle
angle_sum_count = defaultdict(lambda: {'sum_c': 0, 'squared_sum_c': 0, 'count_c': 0, 
                                       'sum_e': 0, 'squared_sum_e': 0, 'count_e': 0})

# Parse the CSV file
with open('fit_parameters.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    #next(reader)  # Skip the header row
    for row in reader:
        angle = float(row[0])
        angle_radians = radians(angle)  # Convert angle to radians
        q = (4 * pi * n / λ) * sin(angle_radians / 2)
        q_squared = q**2  # Square q
        c_value = float(row[3])  # Fetching 'c' value
        e_value = float(row[5])  # Fetching 'e' value
        angle_sum_count[q_squared]['sum_c'] += 1000 / c_value
        angle_sum_count[q_squared]['squared_sum_c'] += (1000 / c_value) ** 2
        angle_sum_count[q_squared]['count_c'] += 1
        angle_sum_count[q_squared]['sum_e'] += 1000 / e_value
        angle_sum_count[q_squared]['squared_sum_e'] += (1000 / e_value) ** 2
        angle_sum_count[q_squared]['count_e'] += 1

# Calculate average and standard deviation for each q^2 value for both Γ1 and Γ2
angle_average_stddev = {}
for q_squared, values in angle_sum_count.items():
    average_c = values['sum_c'] / values['count_c']
    stddev_c = sqrt((values['squared_sum_c'] / values['count_c']) - (average_c ** 2))
    average_e = values['sum_e'] / values['count_e']
    stddev_e = sqrt((values['squared_sum_e'] / values['count_e']) - (average_e ** 2))
    angle_average_stddev[q_squared] = (average_c, stddev_c, average_e, stddev_e)

# Write the averages and standard deviations to Γ1_average.csv and Γ2_average.csv files
with open('Γ1_average.csv', 'w', newline='') as csvfile1, open('Γ2_average.csv', 'w', newline='') as csvfile2:
    writer1 = csv.writer(csvfile1)
    writer2 = csv.writer(csvfile2)
    writer1.writerow(['q^2', 'Average 1000/c', 'Standard Deviation of 1000/c'])
    writer2.writerow(['q^2', 'Average 1000/e', 'Standard Deviation of 1000/e'])
    for q_squared, (average_c, stddev_c, average_e, stddev_e) in angle_average_stddev.items():
        writer1.writerow([q_squared, average_c, stddev_c])
        writer2.writerow([q_squared, average_e, stddev_e])

# Optionally, you can add a section to plot these results, similar to how it was done for Γ1

# Read the data from Γ1_average.csv for plotting
q_squared_values = []
average_c_values = []
stddev_c_values = []
stddev_q_squared_values = []  # To store the standard deviation of q^2 values
with open('Γ1_average.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        q_squared_values.append(float(row[0]))
        average_c_values.append(float(row[1]))
        stddev_c_values.append(float(row[2]))
        stddev_q_squared_values.append(float(row[0]))  # Add q^2 values for consistency

# Calculate standard deviation of q^2 values
average_q_squared = sum(q_squared_values) / len(q_squared_values)
stddev_q_squared = sqrt(sum((q_sq - average_q_squared) ** 2 for q_sq in q_squared_values) / len(q_squared_values))

# Read the data from Γ2_average.csv for plotting
q_squared_values_e = []
average_e_values = []
stddev_e_values = []
stddev_q_squared_values_e = []  # To store the standard deviation of q^2 values
with open('Γ2_average.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        q_squared_values_e.append(float(row[0]))
        average_e_values.append(float(row[1]))
        stddev_e_values.append(float(row[2]))
        stddev_q_squared_values_e.append(float(row[0]))  # Add q^2 values for consistency

# Calculate standard deviation of q^2 values for Γ2
average_q_squared_e = sum(q_squared_values_e) / len(q_squared_values_e)
stddev_q_squared_e = sqrt(sum((q_sq - average_q_squared_e) ** 2 for q_sq in q_squared_values_e) / len(q_squared_values_e))

# Plotting both Γ1 and Γ2 data for comparison
plt.figure(figsize=(10, 8))

# Plotting Γ1
plt.subplot(2, 1, 1)  # Two rows, one column, first plot
plt.errorbar(q_squared_values, average_c_values, yerr=stddev_c_values, fmt='o', color='blue', label='Γ1: 1000/c')
plt.title('Γ1 q^2 vs. Average 1000/c with Standard Deviation')
plt.xlabel('q^2')
plt.ylabel('Average 1000/c')
plt.grid(True)
plt.legend()

# Plotting Γ2
plt.subplot(2, 1, 2)  # Two rows, one column, second plot
plt.errorbar(q_squared_values_e, average_e_values, yerr=stddev_e_values, fmt='o', color='red', label='Γ2: 1000/e')
plt.title('Γ2 q^2 vs. Average 1000/e with Standard Deviation')
plt.xlabel('q^2')
plt.ylabel('Average 1000/e')
plt.grid(True)
plt.legend()

plt.tight_layout()  # Adjusts plot parameters so that all fits into the figure area
plt.show()