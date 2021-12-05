# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 23:53:19 2021

@author: hatziq
"""

import argparse
import joblib
import math
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import pandas as pd
import pickle
import pycountry
import re
import requests
import socket
import whois

from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from profanity_check import predict_prob
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from tensorflow import keras
from tld import get_tld
from urllib.parse import urlparse
from xgboost.sklearn import XGBClassifier

'''
Load model files.
'''
nlp_model = keras.models.load_model('my_model')
random_forest_model = joblib.load("random_forest.pkl")
random_forest_encode_geo_loc = pickle.load(open('rf_geo_loc_encoder.pkl', 'rb')) 
random_forest_encode_tld = pickle.load(open('rf_tld_encoder.pkl', 'rb'))
xgb_model = pickle.load(open("xgb_model.pickle", "rb"))
xgb_encode_tld = pickle.load(open("xgb_model_enc_tld.pkl", "rb")) 

def nlp_model_prediction(link): 
    '''
        Used to get the prediction using the NLP model.
        If benign, class = 1.
        If malicious, class = 0
    '''
    
    # If protocol not specified, assume http
    if 'http' not in link:
        link = r'http://' + link
    
    # Try to get site content
    site_content = ''
    try: 
        f = requests.get(link)
        site_content = f.text
    except Exception as e:
        print('Unable to get content of', link)
        site_content = ''
        
    # Get probability prediction
    site_content = [site_content]
    site_content = np.array(site_content)
    # print(site_content)
    probability = nlp_model.predict(site_content)[0][0]
    # print(probability)
    
    # If < 0.50, predict as 0 ie benign
    if probability < 0.5:
        return('malicious')
    else:
        return('benign')

def clean_url(url):
    '''
        Helper function to clean url to get profanity score
    '''
    url_text = ""
    try:
        domain = get_tld(url, as_object=True)
        domain = get_tld(url, as_object=True)
        url_parsed = urlparse(url)
        url_text= url_parsed.netloc.replace(domain.tld," ").replace('www',' ') +" "+ url_parsed.path+" "+url_parsed.params+" "+url_parsed.query+" "+url_parsed.fragment
        url_text = url_text.translate(str.maketrans({'?':' ','\\':' ','.':' ',';':' ','/':' ','\'':' '}))
        url_text.strip(' ')
        url_text.lower()
    except:
        url_text = url_text.translate(str.maketrans({'?':' ','\\':' ','.':' ',';':' ','/':' ','\'':' '}))
        url_text.strip(' ')
    return url_text

def rf_model_prediction(url, rf_model, tld_encoder, geo_encoder):
    '''
        Used to get the prediction using the Random Forest model.
        If benign, class == 0. If malicious, class == 1.
    '''
    
    # Add http protocol if not present
    if 'http' not in url:
        url = r'http://' + url
        
    parsed_url = urlparse(url)
    http_scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    
    # Get IP Address 
    ip_addr = None
    try: 
        ip_addr = socket.gethostbyname(netloc)
    except Exception as e: 
        pass
    
    # Get IP Address splits
    ip_split_1, ip_split_2, ip_split_3, ip_split_4 = -1, -1, -1, -1
    if ip_addr is not None: 
        ip_split_1 = int(ip_addr.split('.')[0])
        ip_split_2 = int(ip_addr.split('.')[1])
        ip_split_3 = int(ip_addr.split('.')[2])
        ip_split_4 = int(ip_addr.split('.')[3])
        
    # print('IP Address:', ip_split_1, ip_split_2, ip_split_3, ip_split_4)
    
    # Get URL profanity score
    url_cleaned = clean_url(url)
    url_profanity_score = predict_prob([str(url_cleaned)])
    
    # print('URL Profanity Score:', url_profanity_score)
    
    # Get URL length
    url_length = len(url)
    
    # Get geo_loc, whois_complete and tld
    geo_loc, tld, whois_complete = 'Invalid', 'Invalid', False
    if ip_addr is not None: 
        try: 
            w = whois.whois(ip_addr)
            geo_loc = pycountry.countries.get(alpha_2 = w.country)
            geo_loc = geo_loc.name
            
            tld = get_tld(url)
            
            if 'expiration_date' in w and 'creation_date' in w and 'expiration_date' in w:
                whois_complete = True
        except Exception as e: 
            pass
    
    # print('geo_loc:', geo_loc, 'tld:', tld, 'whois_complete:', whois_complete)
    
    # Get HTTPS status
    https_url = r'https://' + netloc
    https_exists = False 
    try: 
        r = requests.get(https_url)
        if 'http' in r.url:
            https_exists = True
    except Exception as e:
        pass
    
    # print('HTTPS STATUS:', https_exists)
    
    # Extract javascript code length and obfuscated code length
    js_code_len, js_obf_code_len = 0, 0
    try: 
        
        # Extract js code
        s = requests.Session()
        soup = BeautifulSoup(s.get(url).content, 'html.parser')
        js_code = ''
        for node in soup.findAll('script'):
            js_code += (''.join(node.findAll(text=True)))
            
        # Get code lengths
        js_code_len = len(js_code)
        js_obf_code_len = js_code_len - sum(len(i) for i in js_code.split())
    except Exception as e:
        pass
    
    # print('JS Code length:', js_code_len, 'Obfuscated code length:', js_obf_code_len)
    
    # Get tld encoded value
    tld_encoded = None
    tld = np.array([[tld]])
    try: 
        tld_encoded = tld_encoder.transform(tld)
    except ValueError:
        tld_encoded = len(tld_encoder.categories_[0]) + 1
        tld_encoded = np.array([[tld_encoded]])
    tld_encoded = float(tld_encoded[0][0])    
    
    # print('tld before:', tld, 'tld_encoded:', tld_encoded)
    
    # Get geo encoded value
    geo_encoded = None
    geo_loc = np.array([[geo_loc]])
    try: 
        geo_encoded = geo_encoder.transform(geo_loc)
    except ValueError: 
        geo_encoded = len(geo_encoder.categories_[0]) + 1
        geo_encoded = np.array([[geo_encoded]])
    geo_encoded = float(geo_encoded[0][0])
    
    # print('geo_loc before:', geo_loc, 'geo_encoded:', geo_encoded)
    
    # Create dataframe with all the values
    values = {
        'url_len': [url_length], 'ip_split_1': [ip_split_1], 'ip_split_2': [ip_split_2], 
        'ip_split_3': [ip_split_3], 'ip_split_4': [ip_split_4], 'geo_loc': [geo_encoded], 
        'tld': [tld_encoded], 'who_is': [int(whois_complete)], 'js_len': [float(js_code_len)], 
        'js_obf_len': [float(js_obf_code_len)], 'https': [int(https_exists)], 
        'url_profanity_score': [url_profanity_score]
    }
    input_data = pd.DataFrame.from_dict(values)
    # print(input_data)
    
    # Do the prediction
    prediction = rf_model.predict(input_data)[0]
    
    # If prediction == 1, is malicious. Else, is benign
    if prediction == 1:
        return('malicious')
    else:
        return('benign')

def xgb_model_prediction(url, xgb_model, tld_encoder):
    '''
        Used to get the prediction using the XGB model.
    '''
    
    # Add http protocol if not present
    base_url = url
    if 'http' not in url:
        url = r'http://' + url
        
    # Parse the URL
    parsed_url = urlparse(url)
        
    # Check if we can use https
    https_url = r'https://' + parsed_url.netloc 
    try:
        r = requests.get(https_url)
        if 'http' in r.url:
            url = https_url
    except Exception as e:
        pass
        
    # Get who_is information
    today = datetime.now()
    whois_exist = False
    days_since_creation, days_since_last_update, days_until_expiration = -1, -1, -1
    
    try: 
        w = whois.whois(url)
        whois_exist = True
        
        # Get days_since_creation
        if 'creation_date' in w: 
                if isinstance(w['creation_date'], list):
                    days_since_creation = (today - w['creation_date'][0]).days
                else: 
                    days_since_creation = (today - w['creation_date']).days
        
        # Get days_since_update
        if 'updated_date' in w: 
                if isinstance(w['updated_date'], list):
                     days_since_last_update = (today - w['updated_date'][0]).days
                else: 
                     days_since_last_update = (today - w['updated_date']).days
                        
        # Get days_until_expiration
        if 'expiration_date' in w: 
                if isinstance(w['expiration_date'], list):
                     days_until_expiration = (w['expiration_date'][0] - today).days
                else: 
                     days_until_expiration = (w['expiration_date'] - today).days
        
    except Exception as e: 
        whois_exist = False
        
    if whois_exist == False: 
        if (days_since_creation != -1) or (days_since_last_update != -1) or (days_until_expiration != -1): 
            whois_exist = True  
            
    # print('WHOIS EXIST:', whois_exist)
    # print('days_since_creation:', days_since_creation, 'days_since_last_update:', days_since_last_update, 
    #     'days_until_expiration:', days_until_expiration)
    
    # Get url length
    url_length = len(str(url))
    
    # Get path length
    path_length = len(urlparse(url).path)
    
    # Get hostname length
    hostname_length = len(urlparse(url).netloc)
    
    # Get first directory legnth
    url_path = urlparse(url).path
    fd_length = 0
    try: 
        fd_length = len(url_path.split('/')[1])
    except:
        fd_length = 0
        
    # Get top level domain length
    tld = get_tld(url, fail_silently = True)
    tld_length = -1
    try: 
        tld_length = len(tld)
    except: 
        tld_length = -1
    
    # Encode tld value
    tld_encoded = None
    tld = np.array([[tld]])
    try: 
        tld_encoded = tld_encoder.transform(tld)
    except ValueError:
        tld_encoded = len(tld_encoder.categories_[0]) + 1
        tld_encoded = np.array([[tld_encoded]])
    tld_encoded = float(tld_encoded[0][0])   
    
    # print('tld:', tld, 'tld_encoded:', tld_encoded)
    
    # Get counts of the various characters
    count_of_dash = url.count('-')
    count_of_at_symbol = url.count('@')
    count_of_question_mark = url.count('?')
    count_of_percentage = url.count('%')
    count_of_fullstop = url.count('.')
    count_of_equals = url.count('=')
    count_of_https = url.count('https')
    count_of_www = url.count('www')
    
    # Get counts of digits
    count_of_digits = 0
    for i in url: 
        if i.isnumeric(): 
            count_of_digits += 1
    
    # Get counts of letters
    count_of_letters = 0
    for i in url:
        if i.isalpha():
            count_of_letters += 1
            
    # Get entropy
    string = url.strip()
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = sum([(p * math.log(p) / math.log(2.0)) for p in prob])
    
    # Get number of parameters
    num_parameters = len(url.split('&')) - 1
    
    # Get number of fragments
    num_fragments = len(url.split('#')) - 1
    
    # Get number of subdomains
    subdomains = url.split('http')[-1].split('//')[-1].split('/')
    num_subdomains = len(subdomains) - 1
    
    # Get number of directories
    count_dir = (urlparse(url).path).count('/')
    
    # Check if IP Address is used in the URL
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    use_of_ip = 0
    if match: 
        use_of_ip = 1
    else: 
        use_of_ip = 0
        
    # Check if a shortening service is used
    is_short_url = 0
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        is_short_url = 1
    else:
        is_short_url = 0
        
    # Convert to binary values
    whois_exist = int(whois_exist)
    
    # Get profanity value
    url_cleaned = clean_url(url)
    url_profanity_score = predict_prob([str(url_cleaned)])
    url_profanity_score = url_profanity_score[0]
    
    # Create a dictionary of input values
    values = {
        'whois_exist': [whois_exist], 'days_since_creation': [days_since_creation], 
        'days_since_last_update': [days_since_last_update], 
        'days_until_expiration': [days_until_expiration], 'url_length': [url_length], 
        'path_length': [path_length], 
        'hostname_length': [hostname_length], 'fd_length': [fd_length], 'tld': [tld_encoded], 
        'tld_length': [tld_length], 'count_of_-': [count_of_dash], 'count_@': [count_of_at_symbol], 
        'count_?': [count_of_question_mark], 'count_%': [count_of_percentage],
        'count_.': [count_of_fullstop],
        'count_=': [count_of_equals],'count_https': [count_of_https],'count_www': [count_of_www],
        'count_digits': [count_of_digits],'count_letters': [count_of_letters],'count_dir': [count_dir],
        'entropy': [entropy],'num_parameters': [num_parameters],'num_fragments': [num_fragments],
        'num_subdomains': [num_subdomains],'use_of_ip': [use_of_ip],
        'is_short_url': [is_short_url], 'url_profanity_score' : [url_profanity_score]
    }
    
    input_data = pd.DataFrame.from_dict(values)
    # print(input_data)
    
    prediction = xgb_model.predict(input_data)
    prediction = prediction[0]
    # print(prediction)
    
    if prediction == 1:
        return 'benign'
    elif prediction == 0:
        return 'malicious'    

def overall_prediction(url): 
    '''
        Does the overall prediction using all 3 models.
    '''
    # If URL does not have a http, add the http and check if a request is possible
    # If so, keep the 'http' inside
    temp_url = ''
    if 'http' not in url: 
        temp_url = r'http://' + url
        is_http_needed = False
        try:
            temp_1 = urlparse(temp_url)
            temp = socket.gethostbyname(temp_1.netloc)
            is_http_needed = True
        except Exception as e:
            is_http_needed = False
        
        if is_http_needed == True:
            url = temp_url
    
    # Check if the URl is active by checking if host name exists
    parsed_url = urlparse(url)
    is_active = False
    ip_addr = None
    try: 
        ip_addr = socket.gethostbyname(parsed_url.netloc)
        is_active = True
    except Exception as e: 
        is_active = False
        
    # Check if a GET request is possible
    get_address = parsed_url.scheme + r'://' + parsed_url.netloc
    try: 
        r = requests.get(get_address)
        if 'http' in r.url:
            is_active = True
    except Exception as e:
        is_active = False
    
        
    # If not active, only use model 3
    if is_active == False:
        prediction = xgb_model_prediction(url = url, 
                      xgb_model = xgb_model, 
                      tld_encoder = xgb_encode_tld)
        return prediction
    else: 
        # Use all 3 models and get a majority vote
        prediction_1 = nlp_model_prediction(url)
        prediction_2 = rf_model_prediction(url = url,  
                    rf_model = random_forest_model,
                    tld_encoder = random_forest_encode_tld, 
                    geo_encoder = random_forest_encode_geo_loc)
        prediction_3 = xgb_model_prediction(url = url, 
                      xgb_model = xgb_model, 
                      tld_encoder = xgb_encode_tld)
        
        # Get majority prediction
        preds = Counter([prediction_1, prediction_2, prediction_3])
        # print(preds)
        majority, count = preds.most_common()[0]
        return majority

def main():
    '''
    Main driver for prediction
    '''
    print('\n')
    
    # Get website from commandline
    parser = argparse.ArgumentParser() 
    parser.add_argument('-w', type = str, required = True)
    args = parser.parse_args()
    url = args.w
    
    prediction = overall_prediction(url)
    print('Prediction for', url, ':', prediction)
    
  

if __name__ == '__main__':
    main()