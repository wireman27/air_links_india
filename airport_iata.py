import sys
sys.path.insert(0, "/Users/user/Documents/Python_Packages")
import wikipedia
import re
import pandas as pd
import copy
import numpy
import json

file_route = '/Users/user/Documents/Cities/India_Air_Links/airline_routes_schedule.csv'
df = pd.read_csv(file_route)
serial = df['Sl. No.'].tolist()
non_iata_loc = list()

counter = 0
for x in serial:
    try:
        check = float(x)
    except ValueError:
        non_iata_loc.append(counter)
    counter = counter + 1

routes = list()


for loc in non_iata_loc:
    try:
        air1 = df.iloc[loc,0]
        start = int(loc) + 1
        if loc == non_iata_loc[-1]:
            end = df.shape[0] - 1
        else:
            end = non_iata_loc[non_iata_loc.index(loc) + 1] - 1           
        for row in range(start, end + 1):
            entry = dict()
            entry['operator']=df.iloc[row,2]
            entry['pt_airport']=serial[loc]
            entry['arr']=df.iloc[row,5]
            entry['dep']=df.iloc[row,7]
            entry['route']=df.iloc[row,11]
            routes.append(entry)
    except Exception as err:
        print(serial[loc], loc, err)
routes_df = pd.DataFrame(routes)


## Temporary for creating lnglatiata database

##iatas = list()
##unique_apt = routes_df['pt_airport'].unique().tolist()

##for apt in unique_apt:
##    entry = dict()
##    entry['pt_apt']=apt
##    entry['lng']='nan'
##    entry['lat']='nan'
##    entry['apt']='nan'
##    try:
##        airport = wikipedia.page(apt + ' airport')
##        searchObj = re.search(r'IATA: ([A-Z]{3})',airport.content)
##        if searchObj:
##            airport_iata = searchObj.group(1)
##            entry['apt']=airport_iata
##        lat_lng = airport.coordinates
##        airport_lat = float(lat_lng[0])
##        airport_lng = float(lat_lng[1])
##        entry['lng']=airport_lng
##        entry['lat']=airport_lat
##    except Exception as err:
##        print(apt, ":", err)
##    iatas.append(entry)   
##        
##iatas_df = pd.DataFrame(iatas)
##iatas_df.to_csv('/Users/user/Documents/Cities/India_Air_Links/airport_iatas.csv')

lnglatiata_df = pd.read_csv('/Users/user/Documents/Cities/India_Air_Links/lnglatiata.csv')

def dupe_check(row):
    if str(row['arr']) == 'nan':
        air2_iata = str(row['dep'])
    else:
        air2_iata = str(row['arr'])
    if air2_iata == 'Mundra':
        air2_iata = 'nan_'+'Mundra'
    if row['pt_airport']=='Mundra' or row['pt_airport']=='Thoise':
        air1_iata = 'nan_'+row['pt_airport']
    else:
        air1_iata = str(lnglatiata_df[lnglatiata_df['pt_airport']==row['pt_airport']].iloc[0,0])
    route = str(row['route'])
    return(air1_iata+"-"+air2_iata+"-"+route)

routes_df['dupe_check']=routes_df.apply(lambda row: dupe_check(row),axis=1)
routes_df.drop_duplicates(subset = ['dupe_check'],keep='first',inplace=True)

f_geojson = list()

for route in routes_df['dupe_check']:
    entry = dict()
    rs = route.split('-')
    entry['air1_iata'] = rs[0]
    entry['air2_iata'] = rs[1]
    entry['route'] = rs[2]
    entry['air1_lat'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[0]].iloc[0,1]
    entry['air1_lng'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[0]].iloc[0,2]
    entry['air2_lat'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[1]].iloc[0,1]
    entry['air2_lng'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[1]].iloc[0,2]
    f_geojson.append(entry)

f_geojson_df = pd.DataFrame(f_geojson)
f_geojson_df.to_csv('/Users/user/Documents/Cities/India_Air_Links/for_geojson.csv')

llidf = lnglatiata_df
fgj = f_geojson_df

geojson = {
    'type': 'FeatureCollection',
    'features': []
    }

for row in range(0,len(llidf.index.tolist())):
    geojson['features'].append({
        'type': 'Feature',
        'properties': {
            'airport_name':llidf.iloc[row,3]
        },
	'geometry': {
            'type': 'Point',
	    'coordinates': [float(llidf.iloc[row,2]), float(llidf.iloc[row,1])]
        }
    })

for row in range(0,len(fgj.index.tolist())):
    geojson['features'].append({
        'type': 'Feature',
        'properties':{},
	'geometry': {
            'type': 'LineString',
	    'coordinates':
            [
                [float(fgj.iloc[row,2]), float(fgj.iloc[row,1])],
                [float(fgj.iloc[row,5]), float(fgj.iloc[row,4])]                                           
            ]
        }
    })

with open('/Users/user/Documents/Cities/India_Air_Links/air_links_t2.geojson', 'w') as f:
    f.write(json.dumps(geojson))




    

    




