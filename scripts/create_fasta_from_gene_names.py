# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 15:16:36 2025
@author: Alexander Kratz
Takes as input a text file of gene names on separate lines.
Searches Ensemble for the gene ID and takes the canonical 
transcript, if present, and saves them into a fasta.

MIT Liscence
"""
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import requests
import argparse
from pathlib import Path
from typing import List

root_dir = Path(__file__).resolve().parent.parent

def get_seq_from_gene_name(gene_name:str)->str:
    #Get the esnt
    server = "https://rest.ensembl.org"
    ext = "/lookup/symbol/homo_sapiens/"+gene_name+"?expand=1"
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    if not r.ok:
      return None
    
    decoded = r.json()
    enst =  decoded['canonical_transcript']
    #Use the enst to get the transcript
    base_id = enst.split('.')[0]
   
    # Ensembl REST API endpoint for sequence
    url = f"https://rest.ensembl.org/sequence/id/{base_id}?type=protein"
   
    # Make the request
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
   
    # Check if request was successful
    if response.status_code != 200:
        return None
   
    # Parse the response
    data = response.json()
   
    # Return the sequence
    return data.get('seq')

def make_fasta(gene_names, output_file):
   records = list()
   for gene in gene_names:
      
      aa_sequence = get_seq_from_gene_name(gene)
      if aa_sequence:
          # Make record
          record = SeqRecord(
              Seq(aa_sequence),
              id=gene,
              name=gene,
              description=""
          )
          records.append(record)

          print(f"Found protein of len {len(record)} for gene: {gene}")
      else:
          print(f"Could not retrieve sequence for gene: {gene}")
   
   # Write all records to the output file
   SeqIO.write(records, output_file, "fasta")

def load_genes(path:str)->List[str]:
   with open(path,'rt') as fh:
      return [l.strip() for l in fh.readlines()]

def main():
   # Set up argument parser
   parser = argparse.ArgumentParser(description='Convert gene names to protein FASTA sequences')
   parser.add_argument('-i', '--input', required=True, help='Input file with gene names (one per line)')
   parser.add_argument('-o', '--output', required=True, help='Output FASTA file')
   
   # Parse arguments
   args = parser.parse_args()
   input_file = args.input
   output_file = args.output
   
   # Process the genes
   genes = load_genes(input_file)
   make_fasta(genes, output_file)

if __name__ == "__main__":
    main()