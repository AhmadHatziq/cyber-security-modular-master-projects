
# Read in KDD train set
filepath <- "C:\\Users\\hatzi\\Documents\\SUTD\\Security Tools Projects\\STL1 - Data Analytics\\Datasets\\KDDTrain_binary_labels.csv"
train_set <- read.csv(filepath)

# Set label as factor
# train_set$xAttack <- factor(train_set$xAttack )

# Load libraries
library(cluster)    # clustering algorithms
library(factoextra) # clustering algorithms & visualization
library(tidyverse)

## Do K-means ----
## Elbow method to find optimal number of clusters ----
# function to compute total within-cluster sum of square 
wss <- function(k) {
  kmeans(train_set, k, nstart = 10 )$tot.withinss
}

# Compute and plot wss for k = 1 to k = 15
k.values <- 1:15

# extract wss for 2-15 clusters
wss_values <- map_dbl(k.values, wss)

plot(k.values, wss_values,
     type="b", pch = 19, frame = FALSE, 
     xlab="Number of clusters K",
     ylab="Total within-clusters sum of squares")

## Regression using R ----

# Use regression of all possible values on the top 5 features
library('olsrr')

model <- lm(xAttack ~ dst_bytes + dst_host_srv_count + 
              logged_in + dst_host_srv_serror_rate + same_srv_rate,
            data = train_set)
k <- ols_step_all_possible(model)
(k)
summary(model)

# Do stepwise regression on all features
require('MASS')
full.model <- lm(xAttack ~., data = train_set)
step.model <- stepAIC(full.model, direction = "both", 
                      trace = FALSE)
summary(step.model)

# Logistic regression modelling ----

# Do with top 5 features
train_set$xAttack <- factor(train_set$xAttack )
logit_model_1 <- glm(formula = xAttack ~ dst_bytes + dst_host_srv_count + 
                       logged_in + dst_host_srv_serror_rate + same_srv_rate,
    family = binomial(link = "logit"), data = train_set)
summary(logit_model_1)


full.glm.model <- glm(xAttack ~.,  family = binomial(link = "logit"), data = train_set)
step.model <- stepAIC(full.glm.model, direction = "both", 
                      trace = FALSE)
summary(step.model)
