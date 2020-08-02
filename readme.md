# Seizure Tracker  

![Build Status](https://github.com/this-josh/seizure_tracker/workflows/deploy-to-eb/badge.svg)


This is a simple Plotly dash app which can be used to view seizure clusters which are read from a csv with the intention being to predict forthcoming seizures. 

The app is currently hosted in an Amazon Web Services Elastic Beanstalk environment and is refreshed using a lambda function.

## Implementation
1. Change the df url in application.py, an example csv can be seen [here]('https://docs.google.com/spreadsheets/d/e/2PACX-1vT1E1Y9IohHUf_WI6bOaJ162ZnRIv39tJbVF8C7Ow0-wqN-DDxslgTfhsUwvQUqoXn-grW89r_BRIyw/pub?gid=0&single=true&output=csv')
2. 