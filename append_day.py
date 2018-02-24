import parse, scraper, dateutil.parser
from datetime import datetime

def run(source, date):
    str_date = dateutil.parser.parse(date).strftime('%m-%d-%Y')
    scraper.scrape(str_date+'.csv', date, date)
    parse.parse_to_csv(str_date+'.csv', str_date+'p.csv')

if __name__ == "__main__":
    run(input("source file: "), input("Date: "))