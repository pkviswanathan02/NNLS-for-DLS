import os
import csv
import warnings
import numpy as np
from scipy.optimize import least_squares

# Suppress warnings 
warnings.filterwarnings('ignore')

# Function for the model y = a + b * exp(-x / c) + d * exp(-x / e)
def biex_function(x, params):
    b, c, d, e = params
    return b * np.exp(-x / c) + d * np.exp(-x / e)

def fit_data(x, y, initial_guess):
    # Define bounds: all parameters must be non-negative
    lower_bounds = [0, 1e-2, 0, 1e-2]  # prevent c, e from being zero to avoid division by zero
    upper_bounds = [np.inf, np.inf, np.inf, np.inf]
    bounds = (lower_bounds, upper_bounds)

    # Use least_squares with bounds
    result = least_squares(lambda params: y - biex_function(x, params),
                           initial_guess, bounds=bounds)
    return result.x  # return the optimal parameters

def process_file(filepath, csv_writer, initial_guess):
    x_data = []
    y_data = []
    try:
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file)
            #next(csv_reader)  # Skip the header row
            for row in csv_reader:
                angle, xval, yval = map(float, row)
                if yval < 0:
                    break
                x_data.append(xval)
                y_data.append(yval)

        # Convert lists to numpy arrays
        x_data = np.array(x_data)
        y_data = np.array(y_data)

        # Perform curve fitting with NNLS
        params = fit_data(x_data, y_data, initial_guess)

        # Write the fitted parameters to CSV file or do whatever you need to do with them
        csv_writer.writerow([angle,os.path.basename(filepath), *params])
        print("Parameters for", os.path.basename(filepath), ":", params)
    
    except Exception as e:
        print(f"Error processing file {os.path.basename(filepath)}: {e}")

def main():
    directory_path = 'g1'
    initial_guess = (0.3, 300, 0.05, 100)  # Initial guess for the fitting parameters
    with open('fit_parameters.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath) and filepath.endswith('.csv'):
                process_file(filepath, csv_writer, initial_guess)

if __name__ == "__main__":
    main()
