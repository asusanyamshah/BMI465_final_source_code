# Importing the necessary libraires
import pandas as pd
import os



from Bio import Entrez

# This is a very important function. It will take the protein accession or protein id and will fetch the taxonomy information of that organism
# I could not download the taxonomy database for mmseq because the file was too big. The zipped file was around 10GB, so I had to use this approach. 
def fetch_ncbi_taxonomy_information(protein_id):

    
    try:
        # Providing my email for the NCBI queries
        Entrez.email = "sshah174@asu.edu"  
        # Searching the protein database
        handle = Entrez.esearch(db="protein", term=protein_id)
        record = Entrez.read(handle)
        handle.close()
        
        if record["IdList"]:
            # Getting protein record
            handle = Entrez.efetch(db="protein", id=record["IdList"][0], rettype="gb", retmode="xml")
            protein_record = Entrez.read(handle)
            handle.close()
            # Extractting organism name
            organism = protein_record[0]["GBSeq_organism"]
            return organism
        return "Unknown"
    except Exception as e:
        return "Unknown"

# This finds out the top 200 hits based on e value and uses the fetch_ncbi_taxonomy_information function to get the organism
def get_top_200_hits_with_taxonomy(file_list, output_dir='filtered_mmseq_results/top_200_hits/'):
    # Making the dir if it doesnt exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Columns of the .m8 file obtainsed from mmseq search
    columns = ['contig', 'subject_id', 'identity', 'alignment_length', 
              'mismatches', 'gap_opens', 'q_start', 'q_end', 
              's_start', 's_end', 'evalue', 'bit_score']
    
    for file_id in file_list:
        try:
            # Reading the .m8 file usng pd.read_csv function, but we set sep = '\t' because istead of commas all the values are seperated using tab
            df = pd.read_csv(f'results_{file_id}.m8', 
                           sep='\t', 
                           header=None, 
                           names=columns)
            
            # Sorting by e-value and get top 20- hits overall
            top_hits = df.sort_values(by=['evalue', 'identity'], ascending=[True, False]).head(200).reset_index(drop=True)
            
            # Adding rank or row column
            top_hits['rank'] = range(1, len(top_hits) + 1)
            
            # Adding the organism information using our previous function
            print(f"\nFetching NCBI taxonomic information for file {file_id}...")
            top_hits['organism'] = top_hits['subject_id'].apply(fetch_ncbi_taxonomy_information)
            
            # Formatting the numerical columns
            top_hits['identity'] = top_hits['identity'].round(2)
            top_hits['evalue'] = top_hits['evalue'].apply(lambda x: f"{x:.2e}")
            
            # Calculating frequency of organisms
            organism_counts = top_hits['organism'].value_counts()
            # Saving results
            output_file = os.path.join(output_dir, f'top_hits_{file_id}.xlsx')
            
            # Creating an Excel writer object to create our excel file as showed in the PPT
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                top_hits[['rank', 'contig', 'subject_id', 'organism', 'evalue', 
                         'identity']].to_excel(writer, 
                                                               sheet_name='Top_Hits', 
                                                               index=False)
                
                # Writing the organism frequency to second sheet. This will help us create graphs
                organism_counts.reset_index().rename(
                    columns={'index': 'Organism', 'organism': 'Count'}
                ).to_excel(writer, sheet_name='Organism_Summary', index=False)
            
            # Printing the summary
            print(f"\nFile {file_id} processed:")
            print(f"Top 20 hits saved with {len(top_hits['organism'].unique())} unique organisms")
            
            
            # Displaying first few entries
            print("\nTop hits:")
            print(top_hits[['rank', 'contig', 'organism', 'evalue', 'identity']].head())
            
        except Exception as e:
            print(f"Error processing file {file_id}: {str(e)}")

# Processing files
files = ['combined']
get_top_200_hits_with_taxonomy(files)
