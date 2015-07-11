#!/bin/sh
wget http://download.geofabrik.de/europe/spain-latest.osm.bz2 
bzip2 -d spain-latest.osm.bze
osm2pgsql -c -s -d osm spain-latest.osm
rm spain-latest.osm
psql -c "DELETE FROM platen_osm_polygon WHERE geom not ST_Intersects(t.geom,geom) FROM( select geom from planet_osm_polygon where admin_level='8' and name ILIKE '$TOWN_NAME') AS t "

