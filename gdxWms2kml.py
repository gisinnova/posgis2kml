#!c:/ms4w/apps/python25/python.exe
# ################################ version 1.0
#Author: geodrinx@gmail.com; gisinnova@gmail.com
# ################################ version 1.0
#Licensed under MIT License. Read the file LICENSE for more information   *
import cgi,sys
import cStringIO
import zipfile
import pg, os, time ,glob
import _gdxvars
pyexe  = _gdxvars.pyexe
server = 'localhost' #_gdxvars.server
uid    = _gdxvars.uid
pwd    = _gdxvars.pwd
service= _gdxvars.service

def maino(x_min, y_min, x_max, y_max, kml1): 

        
        geoxmin=""
        geoymin=""
        geoxmax=""
        geoymax=""
        

        
#CONNESSIONE AL DATABASE            
        db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)
        
        my_user = {"x_min":x_min,"x_max":x_max,"y_min":y_min,"y_max":y_max,"geoxmin":geoxmin,"geoymin":geoymin,"geoxmax":geoxmax,"geoymax":geoymax}

# SELECT  httpmap, layer, nome, descrizione, the_geom  FROM gdxwms;
        
        riga_query = 'SELECT  httpmap, layer, nome, descrizione, gid, ST_XMin(the_geom) as geoxmin, ST_YMin(the_geom) as geoymin, ST_XMax(the_geom) as geoxmax, ST_YMax(the_geom) as geoymax from gdxwms  where ST_Intersects(the_geom, ST_SetSRID(ST_MakeBox2D(ST_Point(%(x_min)s,%(y_min)s),ST_Point(%(x_max)s,%(y_max)s)),4326)) = TRUE order by nome '  %my_user  %my_user
        
        a= db.query(riga_query)
        if len(a.dictresult()) > 0:
              for line in a.dictresult():
                       nome = line['nome']
                       httpmap = line['httpmap']
                       layer = line['layer']

#                       descrizione = line['descrizione']
                       gid = line['gid']
                       
                       geoxmin = line['geoxmin']
                       geoymin = line['geoymin']
                       geoxmax = line['geoxmax']
                       geoymax = line['geoymax']                                                                     
                       
                       kml1 = kml1 +  ('<NetworkLink>\n'
	                       '<name>%s</name>\n'
                         '<visibility>0</visibility>\n'
	                       '<Region>\n'
	                       '<Lod>\n'
	                       '<minLodPixels>128</minLodPixels>\n'
	                       '<maxLodPixels>-1</maxLodPixels>\n'
	                       '</Lod>\n'
	                       '<LatLonAltBox>\n'
	                       '   <west>%s</west>\n'	                       
	                       '   <south>%s</south>\n'
	                       '   <east>%s</east>\n'
	                       '   <north>%s</north>\n'
	                       '</LatLonAltBox>\n'
	                       '</Region>\n'
	                       '<Link>\n'
                         '<href>http://%s/htdocs/python/gdx/gdxWms2kml.py?LINK=%s&amp;LAYERS=%s</href>\n'
#	                       '<href>http://\'+top.location.host+\'/htdocs/python/gdx/gdxWms2kml.py?LINK=%s&amp;LAYERS=%s</href>\n'
                         '<viewRefreshMode>onRegion</viewRefreshMode>\n'
	                       '</Link>\n'
	                       '</NetworkLink>\n'
                         ) %( nome,geoxmin,geoymin,geoxmax,geoymax,server,httpmap,layer ) 
                              

        db.close()
        return kml1




if __name__ == "__main__":

     url = cgi.FieldStorage()
     
     if not (url.has_key("LAYERS")) :
        layers = 'ricerca'
     else:        
        layers = url["LAYERS"].value

     if not (url.has_key("LINK")) :
        link = 'ricerca'
     else:        
        link = url["LINK"].value

     if not (url.has_key("VERSION")) :
        version = '1.1.1'
     else:
        version = url["VERSION"].value


     pos1 = link.find('VERSION=')
     if (pos1 > 0) :
        pos3 = pos1 + 5
        version = link[pos3:pos2]

     if not (url.has_key("REQUEST")) :
        request = 'GetMap'
     else:
        request = url["REQUEST"].value
        
     if not (url.has_key("SRS")) :
        srs = 'EPSG:4326'
     else:        
        srs = url["SRS"].value
        
     if not (url.has_key("WIDTH")) :
        width = '1000'
     else:        
        width = url["WIDTH"].value
        
     if not (url.has_key("HEIGHT")) :
        height = '800'
     else:        
        height = url["HEIGHT"].value
        
     if not (url.has_key("TRANSPARENT")) :
        transparent = 'TRUE'
     else:        
        transparent = url["TRANSPARENT"].value
        
     if not (url.has_key("FORMAT")) :
        format = 'image/png'
     else:        
        format = url["FORMAT"].value
        
     if not (url.has_key("BBOX")) :
        bbox = '7.27,35.92,17.12,47.09'
     else:        
        bbox = url["BBOX"].value 
       
     bbox1 = bbox.split(',')                                                                                                                                                                                                                                                                                                      
     x_min = float(bbox1[0])
     y_min = float(bbox1[1])
     x_max = float(bbox1[2])
     y_max = float(bbox1[3])     

# Url di chiamata a questo applicativo (contiene parametro LINK= che chiama il WMS)
#http://localhost/htdocs/python/gdx/gdxWms2kml.py?LINK=http://localhost/cgi-bin/mapserv.exe?map=f:/gis/htdocs/latina_ecw.map&LAYERS=latina

# Url di chiamata a questo applicativo solo con BBOX=  estrae i wms presenti 
#http://localhost/htdocs/python/gdx/gdxWms2kml.py?BBOX=13.44580165497192,41.15829280839811,13.6657960209164,41.27793601092386


# Url di chiamata al WMS 
#http://localhost/cgi-bin/mapserv.exe?map=f:/gis/htdocs/latina_ecw.map&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=1000&HEIGHT=800&LAYERS=latina&TRANSPARENT=TRUE&FORMAT=image/png&BBOX=13.44580165497192,41.15829280839811,13.6657960209164,41.27793601092386
     
#FieldStorage(None, None, [MiniFieldStorage('LINK', 'http://localhost/cgi-bin/mapserv.exe?map=f:/gis/htdocs/latina_ecw.map'), MiniFieldStorage('VERSION', '1.1.1'), MiniFieldStorage('REQUEST', 'GetMap'), MiniFieldStorage('SRS', 'EPSG:4326'), MiniFieldStorage('WIDTH', '1000'), MiniFieldStorage('HEIGHT', '800'), MiniFieldStorage('LAYERS', 'latina'), MiniFieldStorage('TRANSPARENT', 'TRUE'), MiniFieldStorage('FORMAT', 'image/png'), MiniFieldStorage('BBOX', '13.44580165497192,41.15829280839811,13.6657960209164,41.27793601092386')])
     
     kml =  ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
             '<Document>\n')



     if (link == 'ricerca') :
        kml = kml +('<Folder>\n'
                    '<name>WmsList</name>\n'
                    '	<Style>\n'
                    '		<ListStyle>\n'
                    '			<listItemType>radioFolder</listItemType>\n'
                    '		</ListStyle>\n'
                    '	</Style>\n'
                    '		<Placemark>\n'
                    '			<name>Finestra_WMS</name>\n'
                    '     <visibility>0</visibility>\n'                    
                    '			<Style><PolyStyle>\n'
                    '						<color>7fffffff</color>\n'
                    '			</PolyStyle></Style>\n'                    
                    '			<Polygon>\n'
                    '				<tessellate>1</tessellate>\n'
                    '				<outerBoundaryIs>\n'
                    '					<LinearRing>\n'
                    '						<coordinates>\n'
                    '%s,%s,0 %s,%s,0 %s,%s,0 %s,%s,0 %s,%s,0 </coordinates>\n'
                    '					</LinearRing>\n'
                    '				</outerBoundaryIs>\n'
                    '			</Polygon>\n'
                    '		</Placemark>\n')%( x_min, y_min, x_min, y_max, x_max, y_max, x_max, y_min, x_min, y_min)

        kml1=""
        app = maino(x_min, y_min, x_max, y_max, kml1)

        kml = kml + app + '</Folder>\n'         
         
     else :
        app = ""
        kml = kml + ('<Folder>\n'
             '<name>Elenco Ortofoto test</name>\n'
             '<GroundOverlay>\n'
             '	<name>Wms2Kml_1</name>\n'
             '	<Region>\n'
             '	  <LatLonAltBox>\n'
             '	    <west>%s</west>\n'
             '	    <south>%s</south>\n'
             '	    <east>%s</east>\n'
             '	    <north>%s</north>\n'
             '	  </LatLonAltBox>\n'
             '	</Region>\n'             
             '	<Icon>\n'
             '		<href>%s&amp;VERSION=%s&amp;REQUEST=%s&amp;SRS=%s&amp;WIDTH=%s&amp;HEIGHT=%s&amp;LAYERS=%s&amp;TRANSPARENT=%s&amp;FORMAT=%s&amp;</href>\n'

             '		<viewRefreshMode>onStop</viewRefreshMode>\n'
             '	</Icon>\n'
             '	<LatLonBox>\n'
             '	    <west>%s</west>\n'
             '	    <south>%s</south>\n'
             '	    <east>%s</east>\n'
             '	    <north>%s</north>\n'
             '	</LatLonBox>\n'
             '</GroundOverlay>\n'
             '<GroundOverlay>\n'
             '	<name>Wms2Kml_2</name>\n'
             '	<Region>\n'
             '	  <LatLonAltBox>\n'
             '	    <west>%s</west>\n'
             '	    <south>%s</south>\n'
             '	    <east>%s</east>\n'
             '	    <north>%s</north>\n'
             '	  </LatLonAltBox>\n'
             '	</Region>\n'             
             '	<Icon>\n'
             '		<href>%s&amp;VERSION=%s&amp;REQUEST=%s&amp;SRS=%s&amp;WIDTH=%s&amp;HEIGHT=%s&amp;LAYERS=%s&amp;TRANSPARENT=%s&amp;FORMAT=%s&amp;</href>\n'

             '		<viewRefreshMode>onStop</viewRefreshMode>\n'
             '		<viewRefreshTime>0</viewRefreshTime>\n'
             '	</Icon>\n'
             '	<LatLonBox>\n'
             '	    <west>%s</west>\n'
             '	    <south>%s</south>\n'
             '	    <east>%s</east>\n'
             '	    <north>%s</north>\n'
             '	</LatLonBox>\n'
             '</GroundOverlay>\n'
             '</Folder>\n'                          
             ) %( x_min, y_min, x_max, y_max, link, version, request, srs, width, height, layers, transparent, format, x_min, y_min, x_max, y_max, x_min, y_min, x_max, y_max, link, version, request, srs, width, height, layers, transparent, format, x_min, y_min, x_max, y_max )           
                                      

     kml = kml  + '</Document>\n'     
     kml = kml + '</kml>\n'           
                                      
     print 'Content-Type: application/vnd.google-earth.kml+xml\n'     
     print kml                        
                                                 
                                      

