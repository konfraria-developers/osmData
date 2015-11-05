import psycopg2
from configobj import ConfigObj
import time
import json


def generate_files():

    start = time.time()
    conf = ConfigObj("osmdata.conf")
    osmfilter = "tags->'craft'!='' or shop is not null"
    conn = psycopg2.connect(database=conf['database'],user=conf['user'],password=conf['password'],host=conf['host'])
    print "conected"
    area_sql ="SELECT way FROM planet_osm_polygon where osm_id={0}".format(conf['area_id'])
    groups_sql = "SELECT name,osm_id FROM planet_osm_polygon where admin_level='{0}' and ST_Within(way,({1}))".format(conf['group_admin_level'],area_sql)
    cursor =conn.cursor()
    cursor.execute(groups_sql)
    data = cursor.fetchall()

    print groups_sql
    ids = {}
    for element in data:
        ids[element[1]] = element[0]
    print ids
    ids = { -342960L: 'la Palma de Cervell\xc3\xb3'}
    for identificador in ids.keys():
        print "id:{}".format(identificador)
        print "poblacio:{}".format(ids[identificador])
        wikidata_entites = []
        osm_ids = []
        j = {"type": "FeatureCollection",'features':[]}
        group_sql ="SELECT way FROM planet_osm_polygon where osm_id={0}".format(identificador)
        #wikidata_sql = "select entity,ST_X(geom),ST_Y(geom) from wikidata_entities where geom is not null  and ST_WITHIN(geom,({}))".format(group_sql)
        wikidata_sql = """SELECT entity,ST_X(geom),ST_Y(geom) ,
        (select  title from wikidata_sitelinks where lang='ca'and entity = wikidata_entities.entity ) as name_ca,
        (select  title from wikidata_sitelinks where lang='es'and entity = wikidata_entities.entity  ) as name_es
        from wikidata_entities where geom is not null  and ST_WITHIN(geom,({}));
        """.format(group_sql)
        osm_sql = """(
                        select t.osm_id,ST_X(ST_CENTROID(t.way)) AS x,ST_Y(ST_CENTROID(t.way)) AS y, t.name ,t.shop,t.amenity,t.tags->'craft' from (
                        select st_within(poli.way,polygon.way) inside,poli.*
                        from planet_osm_polygon as poli,(select * from planet_osm_polygon  where planet_osm_polygon.osm_id = {0}) as polygon
                        where poli.tags->'craft'!='' or poli.shop is not null
                        ) as t where inside

                    )
                    UNION
                    (
                        select t.osm_id,ST_X(ST_CENTROID(t.way)) AS x,ST_Y(ST_CENTROID(t.way)) AS y, t.name ,t.shop,t.amenity,t.tags->'craft' from (
                        select st_within(line.way,polygon.way) inside,line.*
                        from planet_osm_line as line,(select * from planet_osm_polygon  where planet_osm_polygon.osm_id = {0}) as polygon
                        where line.tags->'craft'!='' or line.shop is not null
                        ) as t
                        where inside

                    )
                    UNION
                        (
                            select t.osm_id,ST_X(t.way) AS x,ST_Y(t.way) AS y, t.name ,t.shop,t.amenity,t.tags->'craft' from (
                            select st_within(point.way,polygon.way) inside,point.*
                            from planet_osm_point as point,(select * from planet_osm_polygon  where planet_osm_polygon.osm_id = {0}) as polygon
                            where point.tags->'craft'!='' or point.shop is not null
                            ) as t where inside
                        )
                    """.format(identificador,osmfilter)
        print wikidata_sql
        cursor.execute(wikidata_sql)
        data = cursor.fetchall()
        for element in data:
            j['features'].append({'type':'Feature','geometry':{'type':'Point','coordinates':[element[1],element[2]]},'properties': {'name_ca':element[3],'name_es': element[4]} })
            #j['features'].append({'type':'node','id': element[0],'lon':element[1],'lat':element[2],'tags': {'name_ca':element[3],'name_es': element[4]}})
            #wikidata_entites.append(element[0])


        print osm_sql
        cursor.execute(osm_sql)
        data = cursor.fetchall()

        for element in data:
            j['features'].append({'type':'Feature','geometry':{'type':'Point','coordinates':[element[1],element[2]]},'properties': {'name':element[3],'shop': element[4],'craft':element[5]} })
            #j['elements'].append({'type': 'node', 'id': element[0], 'lon':element[1], 'lat':element[2], 'tags': {'name':element[3],'shop': element[4],'craft':element[5]}})
            #osm_ids.append(element[0])
        filename = '{}.json'.format(ids[identificador])
        f = open(filename, 'w')
        f.write(json.dumps(j))
        f.close()

        print "wikidata entities {}".format(wikidata_entites)
        print "osm ids {}".format(osm_ids)
    end = time.time()
    print "time spent:{}".format(end-start)

generate_files()