# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 15:49:00 2025
@author: Alexander Kratz
Processes the output of alphafold pulldown into a csv

MIT Liscence
"""

import json
import os
from glob import glob
import pandas as pd
import pickle
import argparse

def get_dataframe(folder):
    if not os.path.exists(folder):
        print(f"Folder {folder} does not exist")
        quit()
    odf = pd.DataFrame()
    for folder in glob(os.path.join(folder,'*')):
        condition_name = folder.split('/')[-1]
        result_path = os.path.join(folder,'ranking_debug.json')
        if os.path.exists(result_path):
            with open(result_path,'rt') as fh:
                res = json.load(fh)
                best_model  = res['order'][0]
                plddt=pickle.load(open(os.path.join(folder,"result_{}.pkl".format(best_model)),'rb'))['plddt']
                odf.at[condition_name,'average_plddt']=plddt.mean()
                for meta_col in ['iptm','iptm+ptm']:
                    for col in res[meta_col]:
                        odf.at[condition_name,meta_col+'-'+col]=res[meta_col][col]
    return odf

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process output from alphafold pulldown into a csv')
    parser.add_argument('-i', '--input', required=True, help='Directory that contains the results from alphafold pulldown run_multimer_jobs.py')
    parser.add_argument('-o', '--output', required=True, help='Output csv file name')
   
    # Parse arguments
    args = parser.parse_args()
    input_dir = args.input
    output_file = args.output
    df = get_dataframe(input_dir)
    df.to_csv(output_file)
   

if __name__ == "__main__":
    main()