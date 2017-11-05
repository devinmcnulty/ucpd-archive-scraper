import pandas as pd
import numpy as np
import os, sys, time
from pygeocoder import Geocoder

# change current directory to working directory
os.chdir(sys.path[0])

df = pd.read_csv('data/october.csv')

df = df[df["Incident"] != "Void"]

def cut_off_parens(s):
    try:
        return(s[0:(s.index('(') -1)])
    except:
        return s

def geocode(df):
    print("Geocoding...")
    t0 = time.clock()
    lat = []
    lon = []
    api_calls = 0
    for adrs in df["Location"]:
        api_calls += 1
        adrs = cut_off_parens(adrs) + ", Chicago, IL, USA"
        try:
            geo = Geocoder("AIzaSyA_hXZZ_bX38zXKN-OwKMM689uCYOP1SfY").geocode(adrs)
            lat.append(geo.coordinates[0])
            lon.append(geo.coordinates[1])
            
        except:
            lat.append(np.NaN)
            lon.append(np.NaN)
    df['Latitude'] = lat
    df['Longitude'] = lon
    df.to_csv('geocoded.csv')
    print("Geocoding complete. \n" +"Time elapsed: " + str(time.clock() - t0) \
            + "\n" + "API calls made:" + str(api_calls))

types = {"property"  : ["theft","property", "burglary", "damage", "vandalism"],
         "violence"  : ["battery", "robbery", "assualt", "homicide"],
         "substance" : ["liquor", "narcotics", "dui", "cannabis"],
         "medical"   : ["medical", "mental"]}
         
def parse_types(df):
    type_col = []
    for incident in df["Incident"]:
        tag = np.NaN
        for t in types:
            for keyword in types[t]:    
                if keyword.casefold() in incident.casefold():
                    tag = t
                    break
        type_col.append(tag)
                    
    df["Type"] = type_col 
        
    

          
        