# Malicious URL Classification Project 

# Table of Contents
1. [Abstract](#abstract)
2. [Objective](#intro)
3. [Conclusion](#conclusion)
4. [Report](#Report)
5. [Folder Contents](#folder)


## Abstract <a name="abstract"></a>

In this project, we created a malicious URL ensemble
classifier by training on 2 datasets (Dataset of
Malicious and Benign Webpages, Malicious & Benign
URLs). Our ensemble classification model is made up
of 3 different models:

1. A neural network classification model that uses
Natural Language Processing (NLP) and takes
in as input an array of content strings.
2. A random forest classification model.
3. A gradient boosting classification model.

Subsequently, we deployed the malicious URL
classifier via a Chrome extension.

Lastly, the effectiveness of our malicious URL
classifier was evaluated on a third dataset (Malicious
URLs Dataset) which was released around 2 - 3
months ago (24 July 2021). Our model achieved an
overall accuracy of 71.45%.


## Objective <a name="intro"></a>

Cybersecurity attacks present a growing threat to
businesses, governments and individuals. With the
accelerated pace in digital transformation due to the
pandemic, the need for cybersecurity has become
ever more important. In this report, we propose a
method to use machine learning to detect malicious
URLs as an added line of defence.

In this project, two existing datasets are identified to
help train the classification model. The trained
model will then be deployed to test if malicious
URLs are detected via a Chrome Extension. The
effectiveness of our model is assessed with a third,
extremely recent dataset.

We hope that our work will help to make cyberspace
a safer space for all

## Conclusion <a name="conclusion"></a>

In this project, we analyzed 2 malicious URL
datasets (Dataset of Malicious and Benign
Webpages, Malicious & Benign URLs) to better
understand them via data visualizations. After
performing multiple visualisations, we were able to
shortlist these attributes (profanity score, js length,
whois status, http status and web content strings)
which may have a greater factor in determining the
website classification.

Through data visualization, we were able better
understand which of the ten features are more
relevant for our models to train on. The ‘url’,
‘js_len’, ‘js_obf_len’, ‘who_is’, ‘https’ and
‘content’ attributes seem to be able to clearly
differentiate between malicious and benign web
pages with low overlap.

After understanding the 2 datasets, we engineered
more features that will help augment the machine
learning training process. Some of these features
were the usage of IP addresses in the URL, usage of
shortening services and WHO IS domain
information.

Subsequently, we proceeded to the machine learning
process itself. We trained 3 different models: the
NLP neural network, random forest classifier and
gradient boosting classifier.

After we have our trained model, we deployed them
into a back-end flask API with a front-end Chrome
extension. This will help users easily utilize our
model predictions when they are actively browsing.

Next, we used a very recently released third dataset
(Malicious URLs Dataset) to test how accurate our
model was. Our model achieved a 71.45% accuracy,
43.21% recall and 48.25% precision.

Lastly, we addressed our model limitations and gave
some possible strategies that would help increase
our model performance.

## Report <a name="Report"></a>

To view the full report, please click [here](). 

## Folder Contents <a name="folder"></a>

The directory of the folder is as follows:
* /chrome_extension - Files used for the chrome extension.
* /CLI_app - Files used for the CLI application. 
* /machine_learning_code - Code used to train the 3 machine learning models. 
* /pics - Screenshots
* Report.pdf - Report for the project.
* Slides.pdf - Summary slides for the project. 
