import sys
sys.path.insert(0, "/Users/user/Documents/Python_Packages")
import wikipedia
import re
import pandas as pd
import copy
import numpy
import json

file_route = '/Users/user/Documents/Cities/india_air_links_weighted/air_links_india/airline_routes_schedule.csv'
file_capacity = '/Users/user/Documents/Cities/india_air_links_weighted/air_links_india/aircraft_capacities.csv'
df = pd.read_csv(file_route)
capacity_df = pd.read_csv(file_capacity)
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
            entry['aircraft_type'] = df.iloc[row,3]
            entry['frequency'] = df.iloc[row,4]
            routes.append(entry)
    except Exception as err:
        print(serial[loc], loc, err)
routes_df = pd.DataFrame(routes)

def trip_capacity(row):
    if row['frequency']== 'Daily':
        freq = 7
    else:
        freq = len(row['frequency'])
    capa = capacity_df[capacity_df['aircraft_type']==row['aircraft_type']]['capacity']
    return (int(capa * freq))

routes_df['weekly_capacity'] = routes_df.apply(lambda row: trip_capacity(row),axis=1)

lnglatiata_df = pd.read_csv('/Users/user/Documents/Cities/india_air_links_weighted/air_links_india/lnglatiata.csv')

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
clean = routes_df.drop_duplicates(subset = ['dupe_check'],keep='first')

def get_capacity(row):
    unique = row['dupe_check']
    capa = sum(routes_df[routes_df['dupe_check']==unique]['weekly_capacity'])
    return(int(capa))

clean['tot_weekly_capacity'] = clean.apply(lambda row: get_capacity(row),axis=1)

f_geojson = list()

count = 0
for route in clean['dupe_check']:
    entry = dict()
    rs = route.split('-')
    entry['air1_iata'] = rs[0]
    entry['air2_iata'] = rs[1]
    entry['route'] = rs[2]
    entry['twc']= clean.iloc[count,9]
    entry['air1_lat'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[0]].iloc[0,1]
    entry['air1_lng'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[0]].iloc[0,2]
    entry['air2_lat'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[1]].iloc[0,1]
    entry['air2_lng'] = lnglatiata_df[lnglatiata_df['iata_apt']==rs[1]].iloc[0,2]
    f_geojson.append(entry)
    count = count + 1

f_geojson_df = pd.DataFrame(f_geojson)
f_geojson_df.to_csv('/Users/user/Documents/Cities/india_air_links_weighted/air_links_india/for_geojson.csv')

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
        'properties':{
            'rcs': str(fgj.iloc[row,6]),
            'twc': int(fgj.iloc[row,7]),
            'air1': str(fgj.iloc[row,0]),
            'air2': str(fgj.iloc[row,3])
            },
 	'geometry': {
            'type': 'LineString',
            'coordinates':
             [
                 [float(fgj.iloc[row,2]), float(fgj.iloc[row,1])],
                 [float(fgj.iloc[row,5]), float(fgj.iloc[row,4])]                                           
             ]
         }
    })

with open('/Users/user/Documents/Cities/india_air_links_weighted/air_links_india/air_links_t2.geojson', 'w') as f:
    f.write(json.dumps(geojson))




    

    




