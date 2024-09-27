#NAME
#   dataverse_viz
#AUTHOR
#   Emily Zieg, Union of Concerned Scientists (UCS)
#DESCRIPTION
#   Python script to clean up metrics data from UCS Dataverse and visualize it with matplotlib
#   Works in conjunction with dataverse_metrics.sh which runs the curl commands to get the data
#INCLUDED FUNCTIONS
#   read_metrics
#       opens csv file and converts it into a DataFrame
#   by_doi
#       takes metrics DataFrame and returns DataFrame organized by DOI
#   by_date
#       takes metrics DataFrame and returns DataFrame organized by month
#   plot_dl_by_month
#       plots DataFrame from by_date
#   plot_dl_doi
#       plots DataFrame from by_doi

import os
import sys
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def read_metrics(metrics_file):
    #Accepts a filename as argument
    #Returns a DataFrame containing the cleaned data
    date_format = '%Y-%m' #format that the date appears in the csv
    pid = []
    dates = []
    count = []

    try:
        metrics_raw = pd.read_csv(open(metrics_file))
    except:
        print('Unable to read file: ' + metrics_file)
        return()

    for ind in metrics_raw.index:
        try:
            date = metrics_raw.loc[ind, 'date']
            doi = metrics_raw.loc[ind, 'pid']
            dates.append(datetime.datetime.strptime(date, date_format))
            pid.append(doi)
            count.append(metrics_raw.loc[ind, 'count'])
        except:
            print('Unable to convert the following record: ' + metrics_raw.loc[ind])
        
    metrics_data = pd.DataFrame({'date':dates, 'count':count}, index=pid)

    return(metrics_data)

def by_doi(metrics_data):
    #Accepts a DataFrame as argument
    #Returns a DataFrame containing a list of unique DOIs in the dataset and how many times they have been downloaded in descending order
    file_name = 'alltime_dl_by_doi.csv'
    dl_by_doi = []
    doi_index = list(metrics_data.index.drop_duplicates())
    for doi in doi_index:
        alltime_dl_doi = metrics_data.loc[doi]['count'].max()
        dl_by_doi.append(alltime_dl_doi)
    dl_by_doi = pd.DataFrame({'count':dl_by_doi}, index=doi_index).sort_values(by=['count'],ascending=False)
    try:
        dl_by_doi.to_csv(file_name)
        print('Created file ' + file_name)
    except:
        print('Unable to save file ' + file_name)
    return(dl_by_doi)

def by_date(metrics_data):
    #Returns DataFrame of dates and number of downloads for that date
    file_name = 'alltime_dl_by_month.csv'
    date_index = list(metrics_data['date'].drop_duplicates())
    dl_by_date = []
    for month in date_index:
        alltime_dl_monthly = metrics_data[metrics_data['date'] == month]
        dl_by_date.append(alltime_dl_monthly['count'].sum())
    dl_by_date = pd.DataFrame({'count':dl_by_date}, index=date_index)
    try:
        dl_by_date.to_csv(file_name)
        print('Created file ' + file_name)
    except:
        print('Unable to save file ' + file_name)
    return(dl_by_date)

def plot_dl_by_date(metrics_data):
    #Plot the number of downloads over time
    file_name = 'alltime_dl_by_month.pdf'
    fig1, ax1 = plt.subplots(figsize=(9,7))
    ax1.plot(metrics_data, label="Downloads",color="magenta",linestyle="-")
    ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator())
    plt.title('Downloads of UCS Dataverse datasets over time')
    plt.ylabel('Downloads')
    plt.xlabel('Date')
    try:
        plt.savefig(file_name)
        print('Created file ' + file_name)
    except:
        print('Unable to save file ' + file_name)

def plot_dl_doi(doi_data, doi):
    #Plot the downloads over time of a single UCS dataset
    fig2, ax2 = plt.subplots(figsize=(9,7))
    file_name = 'alltime_dl_' + doi[16:] + '.pdf'
    ax2.plot(doi_data.loc[doi, 'date'], doi_data.loc[doi,'count'], label="Downloads",color="magenta",linestyle="-")
    ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax2.xaxis.set_minor_locator(mdates.MonthLocator())
    plt.suptitle('Downloads of ' + doi[4:] + ' over time')
    plt.title('First published ' + str(doi_data.loc[doi, 'date'].min()))  # This is actually the date of first download. Actual publication date should be retrieved from the native API
    plt.ylabel('Downloads')
    plt.xlabel('Date')
    try:
        plt.savefig(file_name)
        print('Created file ' + file_name)
    except:
        print('Unable to save file ' + file_name)

def main(file_name):

    metrics_data = read_metrics(file_name)

    dl_by_doi = by_doi(metrics_data)

    dl_by_date = by_date(metrics_data)

    plot_dl_by_date(dl_by_date)

    plot_dl_doi(metrics_data, dl_by_doi.index[0])

if __name__ == '__main__':
    try:
        directory = str(sys.argv[1])
        os.chdir(directory)
        print('Directory: ' + directory)
    except:
        print('Error: unable to parse argument from command line: directory name')
    try:
        file_name = str(sys.argv[2])
        print('File name: ' + file_name)
    except:
        print('Error: unable to parse argument from command line: file name')
    main(file_name)