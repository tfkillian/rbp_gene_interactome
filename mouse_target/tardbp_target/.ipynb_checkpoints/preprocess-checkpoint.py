import pandas as pd
import re

def convert_binned_sequences(input_file, output_file):
    # Load the provided file
    binned_sequences = pd.read_csv(input_file, sep=',')

    # Extract bin_sequence and create a new DataFrame
    output_df = pd.DataFrame({
        'sequence': binned_sequences['bin_sequence'].apply(lambda x: ' '.join(re.findall('.{1,3}', x.replace('U', 'T')))),
        'label': 0  # Set label to 0 arbitrarily
    })

    # Save to a new file in the dev.tsv format as specified by BERT-RBP
    output_df.to_csv(output_file, sep='\t', index=False)
    print(f"Converted file saved as {output_file}")

if __name__ == "__main__":
    # Process FUS data
    fus_input_file = 'binned_FUS_mouse_target_genes_sequences.csv'
    fus_output_file = 'converted_binned_FUS_mouse_target_genes_sequences.tsv'
    convert_binned_sequences(fus_input_file, fus_output_file)

    # Process TARDBP data
    tardbp_input_file = 'binned_TARDBP_mouse_target_genes_sequences.csv'
    tardbp_output_file = 'converted_binned_TARDBP_mouse_target_genes_sequences.tsv'
    convert_binned_sequences(tardbp_input_file, tardbp_output_file)
