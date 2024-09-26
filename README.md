# Dataverse metrics
## Overview
This project is for retrieving metrics data from the UCS collection in Harvard Dataverse to show the reach of data over time.
## Files
### dataverse_metrics.sh
The main shell script that executes everything. It creates a new directory for the data each time you run it, and runs the python script. 
The directory is named like this:
> dataverse_metrics_YYMMDD_HHMMSS
### dataverse_viz.py
The python script that processes the data and creates some simple plots. It produces 4 files:
- **alltime_dl_by_month.csv**: csv of the total number of downloads of UCS datasets per month since the repository was created
- **alltime_dl_by_month.pdf**: line graph of total downloads over time
- **alltime_dl_by_doi.csv**: csv with a list of all datasets by DOI and the number of times they have been downloaded, descending
- **alltime_dl_XXXXXX.pdf**: line graph of the most downloaded dataset's downloads over time. The file name includes the last six characters of the Dataverse-assigned DOI, which are all under the authority 10.7910/DVN.
