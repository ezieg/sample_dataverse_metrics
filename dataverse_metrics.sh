#!/bin/bash

#Define variables: API key, dataverse instance, API endpoint(s) used, date of request
#export API_KEY= (note to ADS/SciX people: I removed the API key from this script for security reasons; the API can still be accessed without a key, but only public files are visible)
export DATAVERSE_SERVER=https://dataverse.harvard.edu/api
export UNIQUE_DL=info/metrics/uniquedownloads
export NOW=$(date +'%y%m%d_%H%M%S')
export DIR_PATH=dataverse_metrics_$NOW
export FILE_NAME="unique_dl_monthly.csv"

echo $FILE_NAME

#Create directory for the data from this request
mkdir $DIR_PATH

#Get the data from the API (endpoint table in dataverse docs: https://guides.dataverse.org/en/6.3/api/metrics.html#endpoint-table)
curl -o $DIR_PATH/$FILE_NAME $DATAVERSE_SERVER/$UNIQUE_DL/monthly?parentAlias=UCS-DATA

#curl -o $DIR_PATH/unique_dl_alltime.csv $DATAVERSE_SERVER/$UNIQUE_DL/?parentAlias=UCS-Data

#clean up the data to the format we want using a python script
python3 dataverse_viz.py $DIR_PATH $FILE_NAME