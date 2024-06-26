# Load required libraries
library("biomaRt")
library("dplyr")
library("stringr")

## uncomment if you want the full list of genes (not advised!)
# getBM(attributes = c("entrezgene_id", "external_gene_name"),
#       mart = useDataset("mmusculus_gene_ensembl", useMart("ensembl"))) %>%
#   dplyr::rename(entrez_id = entrezgene_id,
#                 gene_symbol = external_gene_name) %>%
#   dplyr::filter(stringr::str_length(entrez_id) > 1,
#                 stringr::str_length(gene_symbol) > 1) %>%
#   as.data.frame() -> mouse_biomart
# saveRDS(object = mouse_biomart, file = "./data/mouse_biomart.rds")

## file path
fp <- "~/Documents/tmp/dacruz/Axonseq_DE_meta_analysis/data/"

## read table of targets
read.table(file = paste0(fp, "selected_FUS_target_genes.txt"), sep = "\t",
           header = FALSE) %>% 
  as.data.frame() -> mouse_gene_symbols

# Placeholder list of unique mouse gene symbols
# mouse_gene_symbols <- c("GeneSymbol1", "GeneSymbol2", "GeneSymbol3")

# Function to fetch DNA sequence for a given gene symbol
fetch_dna_sequence <- function(gene_symbol) {
  # Select the Ensembl mart and dataset
  ensembl <- useMart("ensembl", dataset = "mmusculus_gene_ensembl")
  
  # Query to get the gene sequence
  gene_seq <- getSequence(id = gene_symbol,
                          type = "external_gene_name",
                          seqType = "gene_exon_intron",
                          mart = ensembl)
  
  # Return the DNA sequence
  if (nrow(gene_seq) > 0) {
    return(gene_seq$gene_exon_intron[1])
  } else {
    return(NA)
  }
}

# Create a data frame to store gene symbols and their DNA sequences
gene_data <- data.frame(GeneSymbol = mouse_gene_symbols$V1,
                        DNASequence = NA,
                        stringsAsFactors = FALSE)

# Fetch DNA sequences for each gene symbol
for (i in 1:nrow(gene_data)) {
  gene_data$DNASequence[i] <- fetch_dna_sequence(gene_data$GeneSymbol[i])
}

# Function to convert DNA sequence to complementary RNA sequence
convert_dna_to_complementary_rna <- function(dna_sequence) {
  # Replace each nucleotide with its complement
  rna_sequence <- chartr("ATCG", "UAGC", dna_sequence)
  return(rna_sequence)
}

# Read DNA sequences from a file (one sequence per line)
# dna_sequences <- readLines("dna_sequences.txt")

# Convert each DNA sequence to complementary RNA
gene_data$rna_sequences <- sapply(gene_data$DNASequence, convert_dna_to_complementary_rna)
names(gene_data) <- c("gene_symbol", "gene_dna_sequence", "gene_rna_sequence")


# Save the data frame to a CSV file
gene_data %>%
  dplyr::filter(stringr::str_length(gene_dna_sequence) > 1) %>%
  dplyr::select(-gene_dna_sequence) %>%
  write.table(file = paste0(fp, "FUS_mouse_target_genes_sequences_", Sys.Date(), ".tsv"),
              sep = "\t", row.names = FALSE, col.names = TRUE,
              quote = FALSE)
