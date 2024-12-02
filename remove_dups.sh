# Creating an output directory first
mkdir -p processed_files

# Processing each file
for file in ERR1301443_trimmed.fastq ERR1301451_trimmed.fastq ERR473381_trimmed.fastq ERR473402_trimmed.fastq ERR1301446_trimmed.fastq ERR1301462_trimmed.fastq ERR473384_trimmed.fastq ERR477277_trimmed.fastq; do
    base=$(basename "$file" .fastq)
    
    # Deduplicating using dedupe.sh
    dedupe.sh \
    in="$file" \
    out="processed_files/${base}_deduped.fastq"
done