# Dark Web Analysis Project 

If this repository had proved helpful, or if you have any feedback, do give me a follow on [LinkedIn](https://www.linkedin.com/in/ahmad-hatziq-74a938171/)! 

# Table of Contents
1. [Abstract](#abstract)
2. [Introduction](#intro)
3. [Conclusion](#conclusion)
4. [Report](#Report)
5. [Folder Contents](#folder)


## Abstract <a name="abstract"></a>

In this report, the trends of 6 dark net markets (DNMs) are analyzed using the Kilos dataset.

We analyzed their top vendors and possible reasons for their performances, such as user ratings.
The Kilos dataset is then augmented with the Agora dataset to categorize each vendor according to the
type of items/services sold. With the categorization of vendors, we can identify which vendors are
prevalent in each sub-category.
Lastly, the Kilos dataset is verified using 2 other datasets, the Silk Road 2 dataset and the Darknet Market
Cocaine dataset. Despite being collected at different times, these datasets share a small number of
vendors. The ratings of these common vendors are used to determine if there are any discrepancies with
the Kilos dataset

## Introduction <a name="intro"></a>

Online marketplaces hosted on Tor can provide a wide range of escrow services between buyers and
sellers. This allows for buyers and sellers to transact using Bitcoin or other cryptocurrencies in exchange
for services and products, such as drugs, weapons or hacking services.

As a result, multiple dark net markets (DNMs) had cropped up. The most famous was Silk Road 1,
starting in 2011. Over the years, multiple other DNMs have emerged while older DNMs were taken down.

In this project, we aim to analyze the trends in the 6 major DNMs (Apollon, CannaHome, Empire,
Samsara, Cryptonia, Cannazon) and their associated vendors.

The main datasets that we will be using are as follows:
1. [Kilos dataset](https://www.gwern.net/DNM-archives#kilos). This dataset contains information such as site, vendor, timestamp, score and
value_btc. It is collected from a search engine and contains information about the dark web
vendors along with their item values as well as a review score. It contains data about the vendors
of the 6 DNMs of interest. The dataset is dated from 2018 March to 2020 January.
2. [Agora dataset](https://www.kaggle.com/philipjames11/dark-net-marketplace-drug-data-agora-20142015). This dataset contains similar marketplace data as well as categories, locations
and other remarks. It contains data about the vendors of Agora (another DNM). The dataset is
dated from 2014-2015.

All the code used in this analysis can be found in the accompanying Jupyter notebook file, Dark Web Analysis.ipynb.


## Conclusion <a name="conclusion"></a>

In this report, analysis of the 6 DNMs (from the Kilos dataset) have revealed the following.
1. Overall sales (for each category and DNM site) peaked in the September 2019 to December 2019
time period.
2. The top 3 DNM sites that dominate the categories are:
a. Empire - Counterfeits, Forgeries, Information, Services, Drug Paraphernalia
b. Cannazon - Tobacco, Drugs
c. Apollon - Weapons
3. Most of the top vendors specialized in their own category of items with the exception of
sexyhomer. sexyhomer is involved in the Services, Information and Counterfeits categories.
4. Vendor ratings do have an impact on their lifespans.
5. Vendor ratings only have an impact on bitcoin earnings for the top earning vendors.
6. There are 23 vendors that have migrated from Silk Road 2 (in 2014) to the current 6 DNMs (in 2019).
With these insights, it is hoped law enforcement efforts can be focused on the appropriate DNMs according to their needs. For instance, if there is a need to target Drugs, the Cannazon site can be closely monitored. The top vendors for Drugs can also be focused on and new vendors can be identified, by
analyzing their review ratings.

Furthermore, by understanding the overall trends of the DRMs, it can be ascertained when are the peak periods of traffic. Hence, law enforcement efforts can increase their surveillance during these peak
periods.

Lastly, law enforcement agencies can increase surveillance on vendors that are of particular interest.

These vendors could be the top performing vendors or those with longest lifespans or those that had migrated over from other DNMs, like Silk Road 2

## Report <a name="Report"></a>

To view the full report, please click [here](https://github.com/AhmadHatziq/cyber-security-modular-master-projects/blob/main/Dark%20Web%20Analysis%20Project/Report.pdf). 

## Folder Contents <a name="folder"></a>

The directory of the folder is as follows:
* Dark Web Analysis.ipynb - Jupyter notebook used for the analysis of both datasets. 
* README.md - This file.
* Report.pdf - Final report for this dark web data analytics project. 
