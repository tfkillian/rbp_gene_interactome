# rbp_gene_interactome
The repository contains scripts to create training and testing data for implementing RNA-binding protein (RBP) prediction tools, as well as requirement files to install these tools and scripts to run them.

# Using RBP Gene Interactome Data

This guide outlines the process of preparing and analyzing RNA-binding protein (RBP) gene interactome data.

## 1. Binning the Experimental Data

- Use the `binning.py` script in the respective target folders (e.g., `mouse_target/fus_target/` or `axon_exon_seq/`).
- This script splits long RNA sequences into bins of 100 characters each.
- Run the script to create a CSV file with binned sequences.

## 2. Preparing Data for BERT-RBP

- Use the `preprocess.py` script in the same folder as the binning script.
- This script converts the binned sequences into the format required by BERT-RBP:
  - Replaces 'U' with 'T' in the sequences.
  - Splits sequences into triplets.
  - Creates a TSV file with 'sequence' and 'label' columns.

## 3. Getting Binding Confidence Scores

- Use the preprocessed TSV file as input for BERT-RBP.
- Run BERT-RBP to get binding confidence scores for each bin.
- Save the output as a NumPy (.npy) file.

## 4. Appending Binding Scores to Binned Data

- Use the `augment_data_with_predictions.py` script.
- This script loads the original binned CSV and the NumPy files with binding scores.
- It then adds new columns to the CSV, each corresponding to a different RBP's binding scores.
- The result is a new CSV file with the original binned data plus the binding confidence scores.

By following these steps, you can process raw RNA sequence data into a format suitable for further analysis of RBP binding patterns.
