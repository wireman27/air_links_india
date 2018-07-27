# air_links_india
Indian air links weighted by weekly passenger capacity based on DGCA's published 2018 summer schedule.
<br> <br>
Converting http://dgca.nic.in/dom_flt_schedule/flt_index.htm to a Geojson with all the links connecting Indian cities by air weighted by weekly passenger capacity in number of passengers.

1. Clean everything in the folder Raw DGCA Files using Tabula to give airline_routes_schedule.csv
2. Using airline_routes_schedule.csv, airports.csv, lnglatiata.csv and aircraft_capacities.csv, run airport_iata.py to give for_geojson.py and ultimately air_links_t2.geojson
3. tippecano with -zg on the geojson to give airlinks.mbtiles


