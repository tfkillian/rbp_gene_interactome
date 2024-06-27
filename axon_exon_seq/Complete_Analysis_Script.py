
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Load the new data from the provided CSV file
data_path = '/path/to/your/datafile.csv'  # Update the path to your data file
data = pd.read_csv(data_path)

# Display the first few rows of the dataframe and its summary information
print(data.head())
print(data.info())
print(data.describe())

# Determining high-binding thresholds for motifs analysis
fus_high_threshold = data['FUS'].quantile(0.9)
tardbp_high_threshold = data['TARDBP'].quantile(0.9)

# Filtering data for high binding scores
high_binding_fus = data[data['FUS'] >= fus_high_threshold]
high_binding_tardbp = data[data['TARDBP'] >= tardbp_high_threshold]
print("High FUS Binding Sequences: ", high_binding_fus.shape[0])
print("High TARDBP Binding Sequences: ", high_binding_tardbp.shape[0])

# Finding motifs in sequences
def find_motifs(sequences, motif_length=6):
    motifs = Counter()
    for seq in sequences:
        for i in range(len(seq) - motif_length + 1):
            motif = seq[i:i + motif_length]
            motifs[motif] += 1
    return motifs

# Extracting sequences
high_binding_fus_sequences = high_binding_fus['exon_sequence']
high_binding_tardbp_sequences = high_binding_tardbp['exon_sequence']

# Find frequent motifs in the sequences
fus_motifs = find_motifs(high_binding_fus_sequences, motif_length=6)
tardbp_motifs = find_motifs(high_binding_tardbp_sequences, motif_length=6)

# Extract contexts for the most frequent motifs
def extract_context(sequences, motif, window=10):
    context_data = []
    motif_length = len(motif)
    for seq in sequences:
        start = 0
        while True:
            start = seq.find(motif, start)
            if start == -1:
                break
            start_index = max(0, start - window)
            end_index = min(len(seq), start + motif_length + window)
            context = seq[start_index:end_index]
            context_data.append(context)
            start += motif_length
    return context_data

# Plotting function for motifs
def plot_nucleotide_frequencies(contexts, title):
    context_length = len(contexts[0])
    nucleotide_counts = {i: Counter() for i in range(context_length)}
    for context in contexts:
        for i, nucleotide in enumerate(context):
            nucleotide_counts[i][nucleotide] += 1
    position = np.arange(context_length)
    frequencies = {nucleotide: [nucleotide_counts[i][nucleotide] for i in range(context_length)] for nucleotide in 'ACGT'}
    plt.figure(figsize=(12, 5))
    bottom = np.zeros(context_length)
    for nucleotide, freq in frequencies.items():
        plt.bar(position - context_length//2, freq, bottom=bottom, label=nucleotide, width=1)
        bottom += np.array(freq)
    plt.title(f'Nucleotide Frequencies Around {title}')
    plt.xlabel('Position Relative to Motif Start')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

# Example use
fus_contexts = extract_context(high_binding_fus_sequences, 'TTTTTT')
tardbp_contexts = extract_context(high_binding_tardbp_sequences, 'TGTGTG')

plot_nucleotide_frequencies(fus_contexts, 'FUS (TTTTTT)')
plot_nucleotide_frequencies(tardbp_contexts, 'TARDBP (TGTGTG)')
