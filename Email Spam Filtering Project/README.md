# Email Spam Filtering Project 

If this repository had proved helpful, or if you have any feedback, do give me a follow on [LinkedIn](https://www.linkedin.com/in/ahmad-hatziq-74a938171/)! 

# Table of Contents
1. [Abstract](#abstract)
2. [Introduction](#intro)
3. [Conclusion](#conclusion)
4. [Report](#Report)
5. [Folder Contents](#folder)


## Abstract <a name="abstract"></a>

In this project, we will analyze 2 open-source spam filters: Apache SpamAssassin and Rspamd. We run a [dataset of known phishing](https://monkey.org/~jose/phishing/) emails against these filters and analyze the emails that are **misclassified** as
non-spam.

We run correlation analysis and feature importance (using gradient boosting regressors, where the spam
scores are the target variables and email headers are the predictor variables) to identify email headers that
the 2 open-source spam filters are vulnerable to.

Lastly, we craft an test email using these email headers and test it out on online email services such as
Gmail and Hotmail.


## Introduction <a name="intro"></a>

Spam filters are employed to filter all email traffic and determine if the contents are safe or malicious. If
the filter has determined the content to be unsafe, the incoming email will either be blocked or filtered to
the spam inbox.

The filters can work using a variety of ways. One such way is by whitelisting or blacklisting. Another
way is rule-based scanning of email headers. The last way is by using machine-learning based techniques.
Often, modern spam filters would employ all 3 methods to correctly classify spam emails.

In this project, we will be focusing on 2 email filters: [Apache SpamAssassin](http://spamassassin.apache.org/) and [Rspam](https://rspamd.com/). These are
2 widely used, open-source spam filters. We will be using these spam filters with their default
configurations, rules and without any extra plugins.

Our analysis will focus on the various email headers and resulting spam scores obtained from the 2 email
filters. We will be using an online [email dataset of phishing data](http://monkey.org/~jose/wiki/doku.php) in our analysis.

From the phishing email dataset, we will identify the relevant headers of emails that are wrongly
classified as non-spam by the filters. Subsequently, we will craft another email which makes use of these
headers and test it out on online email services.

The relevant codes and processed datasets can be found in the accompanying folder


## Conclusion <a name="conclusion"></a>

In this project, we tested a dataset of approximately 600 phishing emails against the spam filters
SpamAssassin and Rspamd. Subsequently, we analyzed the column headers that are vital in resulting in
different classifications for both email filters.

Using the column headers, we crafted an email that could fool both SpamAssassin and Rspamd email
filters. However, when the email was sent to online services (Gmail and Hotmail), the online filters were
able to detect the phishing email.

Hence, it is vital for email administrators to not use default configurations of spam filters on their servers.
This is as the default configurations are inadequate in protecting against spam emails. An alternative
would be to use enterprise email filters (such as Google’s filters) which are better equipped to detect spam
emails.

Ideally, email administrators should implement stronger detection mechanisms and test it against the same
dataset that we used. Their test accuracies should be more better than what was obtained with the default
settings (43.181% for SpamAssassin, 44.694% for Rspamd)

## Report <a name="Report"></a>

To view the full report, please click [here](https://github.com/AhmadHatziq/cyber-security-modular-master-projects/blob/main/Email%20Spam%20Filtering%20Project/Report.pdf). 

## Folder Contents <a name="folder"></a>

The directory of the folder is as follows:
* /code 
	* Correlation Analysis & Machine Learning.ipynb - Contains the analysis of results from the rspam and spam_assassin csv files. 
	* generate_rspam_scores.py - Used to generate rspamd_results.csv
	* generate_spam_assassin_scores.py - Used to generate spam_assassin_results.csv
* /csvs - Contains the data generated ie headers present in the test email, classification score and result, true labels. 
	* rspamd_results.csv 
	* spam_assassin_results.csv
* README.md - This file. 
* Report.pdf - Report for the project.
