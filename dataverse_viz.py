#Python script to clean up metrics data from UCS Dataverse and visualize it with matplotlib
#Works in conjunction with dataverse_metrics.sh which runs the curl commands to get the data
#Author: Emily Zieg, Union of Concerned Scientists

#Future projects
# * Get metadata for downloaded datasets

import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Get directory for the data we're using (passed from the python command in dataverse_metrics.sh)
directory = str(sys.argv[1])

#File locations for the API (see dataverse_metrics.sh)
unique_dl_monthly = directory + 'unique_dl_monthly.csv'

date_format = '%Y-%m' #format that the date appears in the csv

#Clean up the data and format the dataframe the way we want
metrics_raw = pd.read_csv(open(unique_dl_monthly)) #file that API data is read from
pid = [] #these lists will be put into the new dataframe
dates = []
count = []

for ind in metrics_raw.index:
    try:
        date = metrics_raw.loc[ind, 'date']
        doi = metrics_raw.loc[ind, 'pid']
        dates.append(datetime.datetime.strptime(date, date_format)) #convert date to datetime object
        pid.append(doi)
        count.append(metrics_raw.loc[ind, 'count'])
    except:
        pass
    
metrics_data = pd.DataFrame({'date':dates, 'count':count}, index=pid) #put the cleaned up data into a new dataframe

#Create lists of the DOIs and dates we're working with to use as indices
unique_doi = list(metrics_data.index.drop_duplicates())
unique_dates = list(metrics_data['date'].drop_duplicates())

#How many times has each dataset been downloaded since it was deposited?
dl_by_doi = []
for doi in unique_doi:
    alltime_dl_doi = metrics_data.loc[doi]['count'].max()
    dl_by_doi.append(alltime_dl_doi)
dl_by_doi = pd.DataFrame({'count':dl_by_doi}, index=unique_doi).sort_values(by=['count'],ascending=False)
most_dl_doi = dl_by_doi.index[0]
dl_by_doi.to_csv(directory + 'alltime_dl_by_doi.csv')

#How many times have UCS datasets been downloaded over time? (cumulative downloads)
dl_by_date = []
for month in unique_dates:
    alltime_dl_monthly = metrics_data[metrics_data['date'] == month]
    dl_by_date.append(alltime_dl_monthly['count'].sum())
dl_by_date = pd.DataFrame({'count':dl_by_date}, index=unique_dates)
dl_by_date.to_csv(directory + '/alltime_dl_by_month.csv')

#Plot the number of downloads over time
fig1, ax1 = plt.subplots(figsize=(9,7))

ax1.plot(dl_by_date, label="Downloads",color="magenta",linestyle="-")
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax1.xaxis.set_minor_locator(mdates.MonthLocator())
plt.title('Downloads of UCS Dataverse datasets over time')
plt.ylabel('Downloads')
plt.xlabel('Date')
plt.savefig(directory + '/alltime_dl_by_month.pdf')

#Plot the downloads over time of a single UCS dataset
fig2, ax2 = plt.subplots(figsize=(9,7))

ax2.plot(metrics_data.loc[most_dl_doi, 'date'], metrics_data.loc[most_dl_doi,'count'], label="Downloads",color="magenta",linestyle="-")
ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
ax2.xaxis.set_minor_locator(mdates.MonthLocator())
plt.suptitle('Downloads of ' + most_dl_doi[4:] + ' over time')
plt.title('First published ' + str(metrics_data.loc[most_dl_doi, 'date'].min()))
plt.ylabel('Downloads')
plt.xlabel('Date')
plt.savefig(directory + '/alltime_dl_' + most_dl_doi[16:] + '.pdf')