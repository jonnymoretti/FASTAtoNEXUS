# FASTA to NEXUS Converter

### Description

This Pyhton script is designed to convert files in te `.fasta` format to the NEXUS format commonly used in phylogenetic analyses. It performs the following functions:

- **Read Fasta File:** `.fasta` file and stores sequences and their respective names in a dictionary.
- **Line Adjustment:** Adjust lines to the right and saves the dictionary to a `.txt` file.
- **Sequence Count:** Counts the number of sequences in the `.fasta` file.
- **Character Count:** Counts the number of characters in each sequence and checks if they all have the same length.
- **Outgroup Identification:** Fletches and returns the specified outgroup, checking if the provided name exists in the file.
- **Nexus File Generation:** Creates a NEXUS file containing information from the dictionary.

### How to Use

#### Requirements

- Python 3.x

#### Execution Command
```
python ConverterFASTAtoNEXUS.py fasta_file outgroup_name ngen_value
```

#### Arguments

1. `fasta_file`: The `.fasta` file you want to convert.
2. `outgroup_name`: The name of the desired outgroup.
3. `ngen_value`: The desired value for the `ngen` parameter used in the `mcmcp` block.

### Example
```
python ConverterFASTAtoNEXUS.py input.fasta outgroup_name 100000
```

### Result

The script will print to the console the content of the generated NEXUS file, which can be copied and pasted into a text file for later use in phylogenetic analysis programs, such as MrBayes.

### Notes

- Ensure you have Python 3.x installed before running the script.
- This script was developed as a quick tool to convert `.fasta` files to the NEXUS format.
