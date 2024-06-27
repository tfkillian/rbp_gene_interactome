import pandas as pd

# Load the TSV files
fus_data = pd.read_csv('FUS_mouse_target_genes_sequences_2024-06-26.tsv', sep='\t')
tardbp_data = pd.read_csv('TARDBP_mouse_target_genes_sequences_2024-06-27.tsv', sep='\t')

# Function to split sequences into bins of maximum 100 characters
def split_sequence(sequence, bin_size=100):
    return [sequence[i:i+bin_size] for i in range(0, len(sequence), bin_size)]

# Function to process data and create binned dataframe
def process_data(data):
    gene_symbols = []
    gene_rna_sequences = []
    bin_sequences = []
    bins = []
    
    for index, row in data.iterrows():
        gene_symbol = row['gene_symbol']
        gene_rna_sequence = row['gene_rna_sequence']
        
        binned_sequences = split_sequence(gene_rna_sequence)
        num_bins = len(binned_sequences)
        
        for bin_number, bin_sequence in enumerate(binned_sequences, start=1):
            gene_symbols.append(gene_symbol)
            gene_rna_sequences.append(gene_rna_sequence)
            bin_sequences.append(bin_sequence)
            bins.append(bin_number)
    
    result_df = pd.DataFrame({
        'gene_symbol': gene_symbols,
        'gene_rna_sequence': gene_rna_sequences,
        'bin_sequence': bin_sequences,
        'bin': bins
    })
    return result_df

# Process FUS data
fus_result_df = process_data(fus_data)
fus_result_df.to_csv('binned_FUS_mouse_target_genes_sequences.csv', sep=',', index=False)

# Process TARDBP data
tardbp_result_df = process_data(tardbp_data)
tardbp_result_df.to_csv('binned_TARDBP_mouse_target_genes_sequences.csv', sep=',', index=False)

print("Processing complete. Files saved as 'binned_FUS_mouse_target_genes_sequences.csv' and 'binned_TARDBP_mouse_target_genes_sequences.csv'")
