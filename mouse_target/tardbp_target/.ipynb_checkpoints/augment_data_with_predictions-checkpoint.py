import pandas as pd
import numpy as np

# Load the numpy arrays
FUS_values = np.load('tardbp_target_mouse_FUS.npy')
TARDBP_values = np.load('tardbp_target_mouse_TARDBP.npy')

# Define the CSV file path and chunk size
csv_file_path = 'binned_TARDBP_mouse_target_genes_sequences.csv'
chunk_size = 1000  # Adjust the chunk size based on your system memory

# Prepare to process the CSV in chunks
reader = pd.read_csv(csv_file_path, chunksize=chunk_size)

# Process each chunk
for i, chunk in enumerate(reader):
    start_index = i * chunk_size
    end_index = start_index + chunk.shape[0]

    # Assign the corresponding numpy values to the new columns in the chunk
    chunk['FUS'] = FUS_values[start_index:end_index]
    chunk['TARDBP'] = TARDBP_values[start_index:end_index]

    # Save each modified chunk to a new CSV file
    if i == 0:
        # Write headers only for the first chunk
        chunk.to_csv('augmented_binned_TARDBP_mouse_target_genes_sequences.csv', index=False, mode='w')
    else:
        # Append without headers for subsequent chunks
        chunk.to_csv('augmented_binned_TARDBP_mouse_target_genes_sequences.csv', index=False, mode='a', header=False)

print("Processing complete. The modified CSV is saved.")
