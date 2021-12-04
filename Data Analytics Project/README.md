# Data Analytics Project 

In this project, a binary classification model is created with the [Network Security Lab - Knowledge Discovery and Data Mining (NSL-KDD)](https://github.com/InitRoot/NSLKDD-Dataset) dataset.

The flow of this project is as follows: 
Data Visualization -> Data Analytics -> Data Modelling 

# Table of Contents
1. [Introduction](#Introduction)
2. [Report](#Report)
3. [Folder Contents](#folder)

## Introduction <a name="Introduction"></a>

From the repository, the NSL-KDD dataset has 2 parts, the training and test sets. They are
available in either .csv or .arff file formats.

The training set has 125,973 rows whereas the test set has 22,543 rows. There are 41 feature
columns along with an associated class label (xAttack).

To keep our analysis unbiased, we will only be analysing the training set file. The test set file will only be used to obtain the test set results for each classification model.

The features of this dataset comes from network data captured and are categorized into 5 labels:
normal, probes, remote-to-local attack, user-to-root attack, denial-of-service attack. The features represent network data such as protocol type, number of failed logins and source bytes.
All of the features have already been converted to integer or floats


## Report <a name="Report"></a>
To view the full report, please click [here](https://github.com/AhmadHatziq/cyber-security-modular-master-projects/blob/main/Data%20Analytics%20Project/Report.pdf). 

## Folder Contents <a name="folder"></a>
The directory of the folder is as follows:
* /code
    * R Code.R - Contains code used for regression modelling in R. 
    * LSTM model.ipynb - Contains code used for a LSTM model in Python. 
	* Data Analytics Project.ipynb - Contains code for the remainder of the analysis. 
* README.md - This file.
* Report.pdf - Final report for this data analytics project. 



