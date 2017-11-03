# -*- coding: utf-8 -*-
### Web scraper for UCPD indcident archive
### Format: scrape([filename.csv], [startdate], [enddate])
### Created by Devin McNulty
import urllib, csv, time, dateutil.parser
from datetime import datetime
from bs4 import BeautifulSoup

# query the website and return html
def scrape_url(url, file_name, writer):
    page = urllib.request.urlopen(url)

    # parse html
    soup = BeautifulSoup(page, "html.parser")

    # find ucpd table
    ucpd_table = soup.find("table", attrs={"class": "ucpd"})

    # make list of table rows
    trs = ucpd_table.find_all("tr")
    
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
        scrape_url("https://incidentreports.uchicago.edu/" \
                    + next_href, file_name, writer)

def scrape(file_name, start, end):
    print("Scraping...")
    t0 = time.clock()
    start = dateutil.parser.parse(start)
    end = dateutil.parser.parse(end)
    
    url = "https://incidentreports.uchicago.edu//incidentReportArchive.php?startDate=" \
            + str(start.month)  \
            + "%2F"             \
            + str(start.day)    \
            + "%2F"             \
            + str(start.year)   \
            + "&endDate="       \
            + str(end.month)    \
            + "%2F"             \
            + str(end.day)      \
            + "%2F"             \
            + str(end.year)     
            
    with open(file_name, 'a', newline='') as csv_file:
        # csv writing tool
        writer = csv.writer(csv_file)
        # write headers
        writer.writerow(["Incident","Location","Reported","Occurred",
                        "Comments / Nature of Fire","Disposition","UCPDI#"])
        # scrape the url, recursively scrapes "next" pages until end                
        scrape_url(url, file_name, writer)
        
        
    print("Scrape complete. \n" +"Time elapsed: " + str(time.clock() - t0))