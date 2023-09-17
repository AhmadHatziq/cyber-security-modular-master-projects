# Network Anomaly Detection Project 

In this project, a home lab environment is created. Various malicious and non-malicious traffic are generated and collected using Wireshark. 

With the collected dataset, various machine learning models are trained and tested. 

The final binary classification model is then deployed as a CLI application. 

If this repository had proved helpful, or if you have any feedback, do give me a follow on [LinkedIn](https://www.linkedin.com/in/ahmad-hatziq-74a938171/)! 

# Table of Contents
1. [Abstract](#abstract)
2. [Report](#Report)
3. [Folder Contents](#folder)
4. [Network Anomaly Detection Tool](#tool)

## Abstract <a name="abstract"></a>

In this project, a lab network environment is set up with multiple machines (via virtual machines). Various services were hosted, such as a HTTP server, Python Flask web application, email server, FTP server and SQLite DB server. 

With these services running, benign traffic packets were generated via scripts and
collected via Wireshark. Similarly, various attacks (such as bruteforce, SQL, XSS, phishing emails, probe, DoS) were carried out and malicious traffic packets were also collected via Wireshark.

With the Wireshark pcap files, cicflowmeter was used to extract relevant features. After traffic generation, we attempt to analyze the data and craft an adequate machine learning model that is capable of detecting future network-based intrusion attacks. Using this data, multiple machine learning models were created
and evaluated. 

Ultimately, the best performing model was the decision tree.
A command-line tool for network anomaly detection was subsequently built using the machine learning model. The tool takes in a pcap file as input and outputs a binary classification: benign or malicious.

## Report <a name="Report"></a>
To view the full report, please click [here](https://github.com/AhmadHatziq/cyber-security-modular-master-projects/blob/main/Network%20Anomaly%20Detection%20Project/Report.pdf). 

## Folder Contents <a name="folder"></a>
The directory of the folder is as follows:
* /machine_learning_code
	* LSTM.ipynb - Jupyter notebook for the LSTM model. 
	* Machine Learning.ipynb - Jupyter notebook for the training of the remaining models. 
* /network_anomaly_detection_tool
	* decision_tree.pickle - Decision tree model used by the tool. 
	* network_anomaly_tool.py - Python file for the CLI detection tool.
* network_data_binary.csv - Dataset collected via the lab network environment. 
* README.md - This file.
* Report.pdf - Final report for this network anomaly detection project. 

## Network Anomaly Detection Tool <a name="tool"></a>

Sample usage on a Linux machine: 
```python3 network_anomaly_tool.py -f INPUT_PCAP_FILE.pcap```


![screenshot of CLI app](https://raw.githubusercontent.com/AhmadHatziq/cyber-security-modular-master-projects/main/Network%20Anomaly%20Detection%20Project/images/image_1.png)

