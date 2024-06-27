import pandas as pd
import numpy as np
import os
import re
import glob

# Define the current working directory
directory_path = os.getcwd()

# Define the CSV file path (update this with the correct path if necessary)
csv_file_path = os.path.join(directory_path, 'Binned_Exon_Sequences.csv')

# Load the CSV file
df = pd.read_csv(csv_file_path)

# Function to extract column name from file name
def extract_column_name(file_path):
    file_name = os.path.basename(file_path)
    column_name = ''.join(re.findall(r'[A-Z0-9]+', file_name))
    return column_name

# Find all .npy files in the current working directory
npy_file_paths = glob.glob(os.path.join(directory_path, '*.npy'))

# Loop through .npy files and add their data to the DataFrame
for npy_file_path in npy_file_paths:
    column_name = extract_column_name(npy_file_path)
    data = np.load(npy_file_path)
    df[column_name] = data

# Save the updated DataFrame to a new CSV file
updated_csv_file_path = os.path.join(directory_path, 'Updated_Binned_Exon_Sequences_All_NPY_Files.csv')
df.to_csv(updated_csv_file_path, index=False)
