#!/bin/sh
wget http://download.geofabrik.de/europe/spain-latest.osm.bz2 
bzip2 -d spain-latest.osm.bze
osm2pgsql -c -s -d osm spain-latest.osm
rm spain-latest.osm

