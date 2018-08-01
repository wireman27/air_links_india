import sys
sys.path.append('/Users/user/Documents/Python_Packages')
import pandas as pd
import json

path = '/Users/user/Documents/Cities/india_air_links_weighted/air_links_india'

data = pd.read_csv(path+ '/for_geojson.csv')

doneRows = set()
finalJson = []
totRows = data.shape[0]

for row in range(totRows):

    if(row in doneRows):
        continue
    
    entry1 = dict()
    entry1["outbound"] = data.iloc[row,8].item()
    entry1["rcs"] = str(data.iloc[row,7])
    entry1['from'] = {
        "name":data.iloc[row,1],
        "coordinates":[
            data.iloc[row,3].item(),
            data.iloc[row,2].item()
            ]
        }
    entry1['to'] = {
        "name":data.iloc[row,4],
        "coordinates":[
            data.iloc[row,6].item(),
            data.iloc[row,5].item()
            ]
        }

    try:
       inv = data[(data['air2_iata']==data.iloc[row,1]) &
                  (data['air1_iata']==data.iloc[row,4])]
       
       test = 3 / inv.shape[0]
       
       entry1["inbound"] = inv.iloc[0,8].item()
       
       entry2 = dict()
       
       entry2["outbound"] = inv.iloc[0,8].item()
       entry2["inbound"] = data.iloc[row,8].item()
       entry2["rcs"] = str(inv.iloc[0,7])
       
       entry2['from'] = {
           "name":inv.iloc[0,1],
           "coordinates": [
               inv.iloc[0,3].item(),
               inv.iloc[0,2].item()
               ]
           }
       entry2['to'] = {
           "name":inv.iloc[0,4],
           "coordinates": [
               inv.iloc[0,6].item(),
               inv.iloc[0,5].item()
               ]
           }
       doneRows.add(inv.iloc[0,0])
       finalJson.append(entry2)
    except:
        x = 2
    finalJson.append(entry1)

with open(path + '/routesJson.json', 'w') as fp:
    json.dump(finalJson, fp)

       
       
                
            
    
    
