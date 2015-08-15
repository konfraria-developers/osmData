#!/bin/sh
#!/bin/bash
wget http://download.geofabrik.de/europe/spain-latest.osm.pbf
osm2pgsql --hstore  --cache 1024 --multi-geometry --number-processes 3 -d osm spain-latest.osm.pbf
rm spain-latest.osm.pbf
psql -c "DELETE FROM platen_osm_polygon WHERE geom not ST_Intersects(t.geom,geom) FROM( select geom from planet_osm_polygon where admin_level='8' and name ILIKE '$TOWN_NAME') AS t "

