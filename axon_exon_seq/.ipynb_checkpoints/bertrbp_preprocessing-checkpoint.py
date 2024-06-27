import pandas as pd
import re

def convert_binned_exon_sequences(input_file, output_file):
    # Load the provided file
    binned_exon_sequences = pd.read_csv(input_file, sep=',')

    # Extract bin_sequence and create a new DataFrame
    output_df = pd.DataFrame({
        'sequence': binned_exon_sequences['bin_sequence'].apply(lambda x: ' '.join(re.findall('.{1,3}', x.replace('U', 'T')))),
        'label': 0  # Set label to 0 arbitrarily
    })

    # Save to a new file in the dev.tsv format as specified by BERT-RBP
    output_df.to_csv(output_file, sep='\t', index=False)
    print(f"Converted file saved as {output_file}")

if __name__ == "__main__":
    input_file = 'binned_exon_sequences.csv'
    output_file = 'converted_binned_exon_sequences.tsv'
    convert_binned_exon_sequences(input_file, output_file)

