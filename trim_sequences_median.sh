# Making a list of sequences and their median scores based on the output of the median_phred.py file
typeset -A median_scores=(
    ["ERR473402"]=39
    ["ERR1301443"]=48
    ["ERR1301451"]=48
    ["ERR473381"]=39
    ["ERR477277"]=39
    ["ERR473384"]=39
    ["ERR1301462"]=47
    ["ERR1301446"]=48
)

# Creating output directory to store the trimmed fastq files if it doesn't exist
mkdir -p trimmed_fastq

# Processing each sequence using a for loop
for seq_id in "${(@k)median_scores}"; do
    # I have to add suffix _merged because all my merged files end in _merged.fastq
    input_file="${seq_id}_merged.fastq"

    median_score=${median_scores[$seq_id]}
    
    # Checking if the input file exists
    if [[ -f "${input_file}" ]]; then
        
        # Trimming with Trimmomatic. The parameters will be discussed in the PPT. 
        java -jar trimmomatic-0.40-rc1.jar SE \
            -phred33 \
            "${input_file}" \
            "trimmed_fastq/${seq_id}_trimmed.fastq" \
            AVGQUAL:${median_score} \
            MINLEN:150
        
        echo "Processed ${seq_id} with median score ${median_score}"
    else
        echo "File ${input_file} not found. Skipping ${seq_id}."
    fi
done

# Printing out the summary
echo "Processing complete. Trimmed files are in 'trimmed_fastq' directory"