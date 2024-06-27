import pandas as pd
import math

# Load the TSV file
file_path = 'top_1000_axonseq_exon_splice_hit_sequences.tsv'
df = pd.read_csv(file_path, sep='\t')

# Function to split sequences into bins of maximum 100 characters
def split_sequence(sequence, bin_size=100):
    return [sequence[i:i+bin_size] for i in range(0, len(sequence), bin_size)]

# Initialize lists to hold the data for the new dataframe
ensembl_exon_ids = []
exon_sequences = []
bin_sequences = []
bins = []

# Iterate over the dataframe and process each sequence
for index, row in df.iterrows():
    ensembl_exon_id = row['ensembl_exon_id']
    exon_sequence = row['exon_sequence']
    
    binned_sequences = split_sequence(exon_sequence)
    num_bins = len(binned_sequences)
    
    for bin_number, bin_sequence in enumerate(binned_sequences, start=1):
        ensembl_exon_ids.append(ensembl_exon_id)
        exon_sequences.append(exon_sequence)
        bin_sequences.append(bin_sequence)
        bins.append(bin_number)

# Create the new dataframe
result_df = pd.DataFrame({
    'ensembl_exon_id': ensembl_exon_ids,
    'exon_sequence': exon_sequences,
    'bin_sequence': bin_sequences,
    'bin': bins
})

if __name__ == "__main__":
    # Save the new dataframe as a csv file
    output_path = 'binned_exon_sequences.csv'
    result_df.to_csv(output_path, sep=',', index=False)
