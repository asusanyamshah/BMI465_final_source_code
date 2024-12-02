import os
import numpy as np

# Setting up my directory. This path might depend based on your computer and where your files are located
directory = 'Trimmomatic/dist/jar/'

# Prefixes of the sequence files of this project
prefixes = ["ERR473384", "ERR473381", "ERR473402", "ERR477277", "ERR1301462", "ERR1301446", "ERR1301451", "ERR1301443"]

# Suffix is added because my merged files end in _merged and are fastq files
suffix = "_merged.fastq"

# Filter files based on prefixes and suffix
files = [file for file in os.listdir(directory) if any(file.startswith(prefix) for prefix in prefixes) and file.endswith(suffix)]

# This function converts the ASCII Phred quality in the sequences to integer score
def ascii_phred_to_score(phred):
    
    return [ord(char) - 33 for char in phred]

# This function calculates and returns the median phred schore
def return_median_phred_score(filename):

    # Here, we are setting up a list to store the phred score of different files
    phred_scores = []

    # Opening the sequence files in read format
    with open(filename, 'r') as f:
        line_count = 0
        for lines in f:

            line_count += 1
            # Only take the 4th line in every 4-line record since it is in FASTQ format
            if line_count % 4 == 0:
                scores = ascii_phred_to_score(lines.strip())
                phred_scores.extend(scores)
    # Calculating the phred score using the numpy median function and returning it if it exists
    return np.median(phred_scores) if phred_scores else None

# Computing the  median Phred score for each file
medians = {file: return_median_phred_score(os.path.join(directory, file)) for file in files}

# Printing the results for use
for file, median in medians.items():
    print(f"{file}: Median Phred Score = {median}")
