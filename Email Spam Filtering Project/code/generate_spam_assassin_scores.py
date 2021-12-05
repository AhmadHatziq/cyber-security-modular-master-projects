#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 15:24:22 2021

@author: kali
"""

import os 
import pandas as pd
import numpy as np
import email
import email.policy
import re
from email.parser import HeaderParser

# Change to email directory
email_folder = r"/home/kali/Desktop/spam_emails/hamnspam"
os.chdir(email_folder)

# Helper function to load a single email file
# Returns a single email object
def load_email(is_spam, filename):
    directory = (email_folder + r'/spam') if is_spam else (email_folder + r'/ham')
    with open(os.path.join(directory, filename), "rb") as f:
        return email.parser.BytesParser(policy=email.policy.default).parse(f)

# Returns counts of headers as a dictionary    
def return_header_counts_as_dict(email_obj, header_set):
    header_dict = dict.fromkeys(header_set, 0)
    
    # Extract email headers from single email
    email_headers = None
    try: 
        email_headers = [x[0] for x in email_obj.items()]
    except Exception as e:
        return header_dict
    
    # Increment counts
    for email_header in email_headers: 
        if email_header in header_dict: 
            header_dict[email_header] += 1
        else:
            pass
            
    return header_dict
        
# Helper function to load Jose's phishing email file (by year)
# Returns a list of email objects
# Eg filename = 'phishing-2020'
def load_jose_dataset(filename): 
    
    # Read raw email lines
    email_list = []
    with open(filename, 'r', encoding="utf8") as f:
        current_email = []
        for line in f: 
            
            # Start of a new email
            if line.startswith("From jose@monkey.org"):
                
                # Store previous email
                email_list.append(current_email)
                
                # Start a new email
                current_email = []
                current_email.append(line)
            else: 
                
                # continue storing current email
                current_email.append(line)
                
    # Convert raw emails to Python email object
    # Parse email data into an email object 
    email_obj_list = []
    for single_email in email_list: 
        
        # Write content to disk 
        with open('email.txt', 'w') as f:
            for item in single_email:
                f.write("%s" % item)
                
        # Read in content to email object 
        with open('email.txt', 'rb') as f:
            email_obj = email.parser.BytesParser(policy = email.policy.default).parse(f)
    
        email_obj_list.append(email_obj)
      
    # Clean up 
    os.remove('email.txt')
    
    return email_obj_list

# Processes the jose dataset, sends to rspam, saves the result to csv
def assasin_jose_dataset(email_list, csv_filename): 
    results_df = pd.DataFrame()
    
    counter = 0
    for single_email in email_list: 
        counter += 1
        
        try: 
        
            # Save email to file 
            with open('email.txt', 'w') as f:
                for item in str(single_email).splitlines():
                    f.write("%s\n" % item)
                    
            # Get header counts
            header_dict = return_header_counts_as_dict(single_email, headers)
            
            # Send file to spamassasin
            os.system('rm email_spamassassin_score')
            os.system('spamassassin email.txt >> email_spamassassin_score') 
                        
            # Read in spam assassins scores
            star_score, spam_status, spam_score = None, None, None
            found_status, found_score = False, False
            with open('email_spamassassin_score', 'r', encoding="utf8", errors='ignore') as f:
                for line in f:   
                    if 'X-Spam-Level' in line: 
                        star_score = (line.split(':')[1]).strip()
                        
                    if 'X-Spam-Status' in line:
                        spam_status = line.split(':')[1]
                        spam_status = (spam_status.split(',')[0]).strip()
                        found_status = True
                        
                        # spam_score = line.split('score=')
                        result = re.search('score=(.*?) required=', line)
                        spam_score = result.group(1)
                        found_score = True
                        
                    if found_score and found_status: 
                        break
                    
            # Store spam scores
            email_info = header_dict
            email_info['spam_status'] = spam_status
            email_info['spam_score'] = spam_score
            
            # Append in dataframe
            results_df = results_df.append(email_info, ignore_index=True)
            
            # Save to file 
            if counter % 10 == 0:
                print(counter)
                results_df.to_csv(csv_filename, index = False)
                
        except Exception as e:
            pass

# Read in the 3 Jose's datasets
jose_2020_emails = load_jose_dataset('phishing-2020')
jose_2019_emails = load_jose_dataset('phishing-2019')
jose_2018_emails = load_jose_dataset('phishing-2018')  

# Pre-process and obtain all possible headers in email dataset
headers = set()
all_emails = jose_2018_emails + jose_2019_emails + jose_2020_emails
for single_email in all_emails: 
    try:   
        email_items = single_email.items()
        for tuple_obj in email_items: 
            headers.add(tuple_obj[0])
    except Exception as e:
        pass

# Get assasin spam scores
assasin_jose_dataset(jose_2020_emails, 'jose_2020.csv')
assasin_jose_dataset(jose_2019_emails, 'jose_2019.csv')
assasin_jose_dataset(jose_2019_emails, 'jose_2019.csv')
