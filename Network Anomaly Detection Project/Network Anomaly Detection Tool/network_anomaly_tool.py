#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 23:34:14 2021

@author: Hatziq
"""

import pandas as pd 
import numpy as np 
import pickle 
import argparse 
import cicflowmeter
import subprocess
import shlex
import os

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

MODEL = 'decision_tree.pickle'

def main():
    
    # Get pcap file from commandline
    parser = argparse.ArgumentParser() 
    parser.add_argument('-f', type = str, required = True)
    args = parser.parse_args()
    pcap_file = args.f
    
    # Load pickle model 
    decision_tree = pickle.load(open(MODEL, "rb"))
    
    # Convert pcap file into csv
    cli_command = 'cicflowmeter -f {} -c input.csv'.format(pcap_file)
    args = shlex.split(cli_command)
    output = subprocess.check_output(args)
    
    # Read in input file 
    input_df = pd.read_csv('input.csv')
    test_rows = input_df[['src_port', 'dst_port', 'protocol', 'flow_duration', 'flow_byts_s',
       'flow_pkts_s', 'fwd_pkts_s', 'bwd_pkts_s', 'tot_fwd_pkts',
       'tot_bwd_pkts', 'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max',
       'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std',
       'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean',
       'bwd_pkt_len_std', 'pkt_len_max', 'pkt_len_min', 'pkt_len_mean',
       'pkt_len_std', 'pkt_len_var', 'fwd_header_len', 'bwd_header_len',
       'fwd_seg_size_min', 'fwd_act_data_pkts', 'flow_iat_mean',
       'flow_iat_max', 'flow_iat_min', 'flow_iat_std', 'fwd_iat_tot',
       'fwd_iat_max', 'fwd_iat_min', 'fwd_iat_mean', 'fwd_iat_std',
       'bwd_iat_tot', 'bwd_iat_max', 'bwd_iat_min', 'bwd_iat_mean',
       'bwd_iat_std', 'fin_flag_cnt', 'down_up_ratio', 'pkt_size_avg',
       'init_fwd_win_byts', 'init_bwd_win_byts', 'active_max', 'active_min',
       'active_mean', 'active_std', 'idle_max', 'idle_min', 'idle_mean',
       'idle_std', 'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'bwd_byts_b_avg',
       'bwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_blk_rate_avg',
       'fwd_seg_size_avg', 'bwd_seg_size_avg', 'subflow_fwd_pkts',
       'subflow_bwd_pkts', 'subflow_fwd_byts', 'subflow_bwd_byts']].copy()
    
    # Do prediction
    test_rows['prediction'] = decision_tree.predict(test_rows)
    
    # Return final classification
    votes = test_rows[['prediction']].value_counts()
    if votes[0] > votes[1]: 
        print('{} is classified as benign'.format(pcap_file))
    else: 
        print('{} is classified as malicious'.format(pcap_file))
        
    # Clean up and delete input.csv
    os.remove('input.csv')
    

if __name__ == '__main__':
    main()