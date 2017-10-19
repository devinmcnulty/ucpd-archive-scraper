# -*- coding: utf-8 -*-
# import libraries
import urllib, csv, dateutil.parser
from datetime import datetime
from bs4 import BeautifulSoup

# query the website and return html
def scrape(url, file_name):
    page = urllib.request.urlopen(url)

    # parse html
    soup = BeautifulSoup(page, "html.parser")

    # find ucpd table
    ucpd_table = soup.find("table", attrs={"class": "ucpd"})

    # make list of table rows
    trs = ucpd_table.find_all("tr")

    # open a csv file with append, so old data not erased
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # loops through table rows in trs
        for tr in trs:
            # list of all tds in table row
            tds = tr.find_all("td")
            row = []
            # loops through individual tds in list tds
            for td in tds:
                # appends text of td to row to be written
                row.append(td.text.strip())
            # writes row to file, excluding blank rows
            if (row != [] and row != [':', '', '', '', '', '', '']):
                writer.writerow(row)
    
    # gets li object for next page button
    next_li = soup.find("li", attrs={"class": "next"})
    
    # a tag in li obj
    next_a = next_li.find("a")
    
    # gets href to next page
    next_href = next_a.get("href")
    
    # if not empty (last page) scrapes next page
    if (next_href != ""):
        scrape("https://incidentreports.uchicago.edu/" + next_href, file_name)

def scrape_dates(file_name, start, end):
     start = dateutil.parser.parse(start)
     end = dateutil.parser.parse(end)
     url = "https://incidentreports.uchicago.edu//incidentReportArchive.php?startDate=" \
            + str(start.month)  \
            + "%2F"             \
            + str(start.day)    \
            + "%2F"             \
            + str(start.year)   \
            + "&endDate="       \
             + str(end.month)   \
            + "%2F"             \
            + str(end.day)      \
            + "%2F"             \
            + str(end.year) 
            
     scrape(url, file_name)

    
url1 = "https://incidentreports.uchicago.edu/incidentReportArchive.php?reportDate=1508216400"
url2 = 'https://incidentreports.uchicago.edu//incidentReportArchive.php?startDate=1508216400&endDate=1508216400&offset=5'    
url3 = "https://incidentreports.uchicago.edu//incidentReportArchive.php?startDate=10%2F10%2F2017&endDate=10%2F17%2F2017"
url4 = "https://incidentreports.uchicago.edu//incidentReportArchive.php?startDate=09%2F17%2F2017&endDate=10%2F17%2F2017"
url5 = "https://incidentreports.uchicago.edu//incidentReportArchive.php?startDate=10%2F17%2F2016&endDate=10%2F17%2F2017"
#scrape(url5, 'year-to-date.csv')

scrape_dates("october3.csv", "2017-10-01", "2017-10'18")


