#This takes the list of gene names from the example_data folder and finds the canonical transcripts for them
#If your proteins of interest do not have gene names, this may not work, but it's a nice utility script.
#If you already have a .fasta of proteins of interest, then you DO STILL need to produce a .txt file with 
#the names of the proteins in the .fasta
python scripts/create_fasta_from_gene_names.py -i example_data/baits.txt -o example_data/baits.fasta
python scripts/create_fasta_from_gene_names.py -i example_data/preys.txt -o example_data/preys.fasta


#These commands create features for each monomer that are used later in the process.
create_individual_features.py  --db_preset reduced_dbs --fasta_paths=example_data/baits.fasta  --data_dir ~/nfs/shr/alphafold_data/  --output_dir=individual_features  --max_template_date=2050-01-01 --use_mmseqs2=True
create_individual_features.py  --db_preset reduced_dbs --fasta_paths=example_data/preys.fasta  --data_dir ~/nfs/shr/alphafold_data/  --output_dir=individual_features  --max_template_date=2050-01-01 --use_mmseqs2=True

#This actually performs the alphafold pulldown process, 
run_multimer_jobs.py --mode=pulldown \
    --protein_lists example/preys.txt,example/baits.txt \
    --data_dir ~/nfs/shr/alphafold_data \
    --monomer_objects_dir individual_features \
    --output_path example_afp_output

#This is a helper function that summarizes all results from a folder into a .csv
python scripts/process_res.py -i example_afp_output -o example_processed_output.csv