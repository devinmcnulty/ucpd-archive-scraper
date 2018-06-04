# UCPD Incidents Archive Scraper
Web scraper for UCPD Daily Incidents Report Archive

Live beta here: https://devinmcnulty.github.io/ucpd-incident-map/map/

To scrape entries between two dates, call function
~~~~ 
scraper([filename.csv], [startdate], [enddate])
~~~~

For example,
~~~~ 
scraper("october-17.csv", "2017-10-01", "2017-1-31")
~~~~
