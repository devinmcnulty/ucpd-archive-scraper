import pandas as pd
import numpy as np
import os, sys, time
from pygeocoder import Geocoder

# change current directory to working directory
os.chdir(sys.path[0])

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
    print("Geocoding complete. \n" +"Time elapsed: " + str(int(time.clock() - t0)) \
            + "\n" + "API calls made:" + str(api_calls))

class Type:
    def __init__(self, name, keywords, marker):
        self.name = name
        self.keywords = keywords
        self.marker = marker


types = [Type("property", ["theft","property", "burglary", "damage", "vandalism"],"large_yellow"),
         Type("violence", ["battery", "robbery", "assualt", "homicide"], "large_red"),
         Type("substance", ["liquor", "narcotics", "dui", "cannabis"], "large_green"),
         Type("medical", ["medical", "mental"], "large_blue")]
         
def parse_types(df):
    print("Parsing types")
    type_col = []
    marker_col = []
    for incident in df["Incident"]:
        tag = "Other"
        marker = "large_purple"
        for t in types:
            for keyword in t.keywords:    
                if keyword.casefold() in incident.casefold():
                    tag = t.name
                    marker = t.marker
                    break
        type_col.append(tag)
        marker_col.append(marker)
                    
    df["Type"] = type_col 
    df["Marker"] = marker_col
        
    
def parse_to_csv(source, output):
    df = pd.read_csv(source)
    df = df[df["Incident"] != "Void"]
    geocode(df)
    parse_types(df)
    df.to_csv(output)
    
if __name__ == "__main__":
    parse_to_csv(input("Source filename: "), input("Output filename: "))