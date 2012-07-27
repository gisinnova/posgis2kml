#!c:/ms4w/apps/python25/python.exe
# ################################ version 1.0
#Author: geodrinx@gmail.com; gisinnova@gmail.com
# ################################ version 1.0
#Licensed under MIT License. Read the file LICENSE for more information   *
# crea un kml con i layer presenti sulla base dati
# i layer vengono prospettati con gli style predefiniti nella tabella gdx_feature
# 

import cgi,sys
import cStringIO
import zipfile
import pg, os, time ,glob
import time
import _gdxvars
pyexe  = _gdxvars.pyexe
server = 'localhost' #_gdxvars.server
uid    = _gdxvars.uid
pwd    = _gdxvars.pwd
service= _gdxvars.service
#pyexe = 'py'        # oppure  'py'
#server = 'localhost'
#uid="postgres"
#pwd="postgres"
#service="postgis2_copy"


descrizione = ""

def disegna(gdxtabella, x_min,y_min,x_max,y_max, kml1, features, idfea):
 

#CONNESSIONE AL DATABASE            

        db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)

# http://server/htdocs/Python/gdx/styles/gdxstyles.kml#PC


        my_user0 = {"gdxtabella":gdxtabella}   
        riga_query0 = "SELECT graphics, azione, condizione, tooltips, extrusion, timeout from gdx_features where tabella = '%(gdxtabella)s' " %my_user0

        riga_query0 = riga_query0 + " and nome = \'%s\' " %(features)

        if idfea > 0:
           riga_query0 = riga_query0 + " and idfea = %s " %(idfea)        

        graphics = "#BLU"
        azione = "gdxLayerBaloon" 
        condizione = ""
        tooltips   = ""
        extrusion  = ""
        altezza    = ""                
                
        a0 = db.query(riga_query0)
        if len(a0.dictresult()) > 0:
           for line in a0.dictresult():

              if line == None:
                 azione = "gdxLayerBaloon"
              else:
                 azione = line['azione']
                 
              if line == None:
                 graphics = "#BLU"
              else:
                 graphics = line['graphics']
              if graphics == None:
                 graphics = "#BLU" 
                 
              if line == None:
                 condizione = ""
              else:
                 condizione = line['condizione']
              
              if line == None:
                 tooltips = "gid"
              else:
                 tooltips = line['tooltips']
              if tooltips == None:
                 tooltips = "gid"
                 
              if line == None:
                 extrusion = ""
              else:
                 extrusion = line['extrusion']
              if extrusion == None:
                 extrusion = ""

              if line == None:
                 timeout = ""
              else:
                 timeout = line['timeout']
              if timeout == None:
                 timeout = ""                                                                  

        pos1 = graphics.find('<StyleMap id=')
        if (pos1 > 0) :
            pos2 = graphics.find('">', pos1)
            pos3 = pos1 + 14
            linea = graphics[pos3:pos2]
            kml1 = kml1 +  ('%s') %( graphics )
            graphics = "#" + linea

        pos1 = graphics.find('<Style id=')
        if (pos1 > 0) :
            pos2 = graphics.find('">', pos1)
            pos3 = pos1 + 11
            linea = graphics[pos3:pos2]
            kml1 = kml1 +  ('%s') %( graphics )
            graphics = "#" + linea


#                                      #  0123456789  12
        if (graphics[:5] == "#GDX_"):  #  #GDX_7f00ffff

            fill   = graphics[-8:]
            empty  = fill[:2]

            codcol = graphics[-6:]

            graphics = "#GDX_" + codcol + "_HILITE"

            kml1 = kml1 +('<Style id="GDX_%s_normale">\n') %(codcol)

            kml1 = kml1 +('		<LineStyle>\n'
                    '			<color>ff%s</color>\n') %(codcol) 

            kml1 = kml1 +('			<width>2.0</width>\n'
                    '		</LineStyle>\n'
                    '	<PolyStyle>\n')

            if (empty != '00'):                    
               kml1 = kml1 +('		<color>%s</color>\n') %(fill)
            else:
               kml1 = kml1 +('		<color>ff%s</color>\n') %(codcol) 
               kml1 = kml1 +('		<fill>0</fill>\n')

            kml1 = kml1 +('	</PolyStyle>\n'
                    '	</Style>\n'
                    '	<Style id="GDX_%s_h1">\n') %(codcol) 

#            kml1 = kml1 +('		<LabelStyle>\n'
#                        '			<scale>0</scale>\n'
#                        '			<text>$[description]</text>\n'
#                        '			<color>ff80ffff</color>\n'
#                        '		</LabelStyle>\n')

            kml1 = kml1 +('		<LineStyle>\n'
                    '			<color>ff%s</color>\n') %(codcol) 


            if (empty != '00'):                    
               kml1 = kml1 +('			<width>4.6</width>\n'
                    '		</LineStyle>\n'
                    '	<PolyStyle>\n')
               kml1 = kml1 +('		<color>%s</color>\n') %(fill)
            else:
   
               kml1 = kml1 +('			<width>3.3</width>\n'
                    '		</LineStyle>\n'
                    '	<PolyStyle>\n')
               kml1 = kml1 +('		<color>ff%s</color>\n') %(codcol) 
               kml1 = kml1 +('		<fill>0</fill>\n')
               
            kml1 = kml1 +('	</PolyStyle>\n'
                    '	</Style>\n'
                    ' <StyleMap id="GDX_%s_HILITE">\n') %(codcol) 

            kml1 = kml1 +('		<Pair>\n'
                    '			<key>normal</key>\n' 
                    '			<styleUrl>#GDX_%s_normale</styleUrl>\n') %(codcol)
                     
            kml1 = kml1 +('		</Pair>\n'
                    '		<Pair>\n'
                    '			<key>highlight</key>\n' 
                    '			<styleUrl>#GDX_%s_h1</styleUrl>\n') %(codcol)
                     
            kml1 = kml1 +('		</Pair>\n'
                    '	</StyleMap>\n')
            
        tempoIniziale = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
#        timeTuple1 = time.strptime(tempoIniziale, "%m/%d/%y %I:%M:%S%p")
        timeTuple1 = time.strptime(tempoIniziale, "%Y/%m/%d %H:%M:%S")
                    
        kml1 = kml1 + ' <Folder>\n'
        
#        kml1 = kml1 + '  <name>%s_%s_%s</name>\n' %(features, idfea, tempoIniziale)
        kml1 = kml1 + '  <name>%s_%s</name>\n' %(features, idfea)        
                       
        my_user = {"gdxtabella":gdxtabella,"x_min":x_min,"x_max":x_max,"y_min":y_min,"y_max":y_max}
        
        riga_query = 'SELECT gid, askml(ST_Reverse(a.the_geom),15) as geo'
        
        if (tooltips != ""):
           riga_query = riga_query + (', %s as tooltip') %(tooltips)
                   
                   
        if (extrusion != ""):        
           riga_query = riga_query + (', %s as altezza') %(extrusion)        
        else:
          riga_query = riga_query + (', 0 as altezza')
          
        riga_query = riga_query + ' from "%(gdxtabella)s" a where a.the_geom && ST_SetSRID(ST_MakeBox2D(ST_Point(%(x_min)s,%(y_min)s),ST_Point(%(x_max)s,%(y_max)s)),4326)'  %my_user  %my_user
                 
        if (condizione != None)and (condizione != '') :                 
           riga_query = riga_query + " AND %s " %(condizione)                
                 
        a = db.query(riga_query)

        if len(a.dictresult()) > 0:
                
           for line in a.dictresult():
               kml_geo = line['geo']
               
               tooltip = line['tooltip']
               
               if (tooltip != None):
                  if (type(tooltip) == 'str'):
                     tooltip = tooltip.replace(chr(7)," ") 

               if line == None:
                 altezza = 0
               else:
                 altezza = line['altezza']
               if altezza == None:
                 altezza = 0 
                 
                     
               if (altezza != 0):
                  kml_geo = kml_geo.replace("<Polygon>","<Polygon>\n<extrude>1</extrude>\n<altitudeMode>relativeToGround</altitudeMode>\n'")                              
                  kml_geo = kml_geo.replace(" ",","+str(altezza)+" ")
                  kml_geo = kml_geo.replace("</coordinates>",","+str(altezza)+"</coordinates>")                               
               
               kml_geo = kml_geo.replace("</LineString>","<tessellate>1</tessellate></LineString>")
               gid = line['gid']

               tempoParziale = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

               timeTuple2 = time.strptime(tempoParziale, "%Y/%m/%d %H:%M:%S")
               time_difference = time.mktime(timeTuple2) - time.mktime(timeTuple1)
               
               if (int(time_difference) < int(timeout)):
        
                  kml1 = kml1 +  (' <Placemark>\n')
#                     '  <name>%s_%s</name>\n' 
                     
#                     ' <description></description>\n'   
#                     ' <Style>\n'
##                    '  <Icon>\n'
##                    '   <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png</href>\n'
##                    '  </Icon>\n' 
#                     '  <BalloonStyle>\n'
##                     '  <text><![CDATA[<big><span style="font-weight: bold;"></span></big>\n') %( tooltip, tempoParziale, graphics )
#                     '  <text><![CDATA[<big><span style="font-weight: bold;"></span></big>\n') %( tooltip, graphics )
                  
                  if azione != None:
                     if application == '':
                       kml1 = kml1 +  ( '  <name>%s</name>\n'
                             '<styleUrl>%s</styleUrl>\n'
                             ' <description><![CDATA[ \n') %( tooltip, graphics )
                       kml1 = kml1 + ('<div name="main" ><iframe  target="main" src= "http://%s/htdocs/python/gdx/%s.py?tabella=%s&gid=%s" height="900%%"  ><p> <a href="http://%s/htdocs/python/gdx/%s.py?tabella=%s&gid=%s" target="main"></p>attributi</iframe></div> \n') %( server, azione, gdxtabella, gid, server, azione, gdxtabella, gid  )
                     else:
                       simo_user = {"tabella":gdxtabella,"gid":gid}
                       simo_query = 'SELECT * from "%(tabella)s" where gid = %(gid)s '   %simo_user
                       qresult= db.query(simo_query)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                       listOfResults = qresult.getresult()
                       listOfFields  = qresult.listfields()
                       kml1 = kml1 + (' <name></name>\n<styleUrl>%s</styleUrl>\n <description><![CDATA[ \n<head><script type="text/javascript" src="http://%s/htdocs/python/gdx/tabber.js"></script><link rel="stylesheet" href="http://%s/htdocs/python/gdx/example.css" type="text/css" media="screen">')%(graphics,server,server)
                       kml1 = kml1 + ('</head>\n<body><form  method="get|post" enctype="multipart/form-data" name="hcc" >\n<div class="tabber">\n' ) 
                       i = 0                          
                       quanti = qresult.ntuples() 
                       conta_url = 0
                       conta_campi=0 
                       for campo in listOfFields:
                         for line in listOfResults:
                            if (str(campo) != "the_geom") and (str(campo[:3]) != "url")  : 
	                                conta_campi = conta_campi + 1
	                                if conta_campi ==1 :
	                                   kml1 = kml1 +('<h6>%s </h6>\n') %tooltip
	                                   kml1 = kml1 +('<div class="tabbertab" style="background: #DDE;border: 1px solid #778;margin-left: 3px;color: #778;"> \n<h5>Informazioni </h5>\n<table>\n') 
	                                if (str(campo) != "DESCR"):
	                                      valore = line[i]
	                                      if (str(valore) != "None"):
	                                          kml1 = kml1 + '<tr> <td style="font-weight:bold;font-family: Trebuchet MS;font-size:7pt;text-decoration: none;">  ' + str(campo) + '</td><td style="font-family: Trebuchet MS;font-size:7pt;text-decoration: none;">' + str(valore) + ' </td></tr>\n'

                            if (str(campo[:3]) == "url")and (str(valore) != "None"): 
	                               conta_url = conta_url + 1
	                               valore = line[i]
	                               if conta_url == 1 :
	                                   if (str(valore) != "None"):
	                                      kml1 = kml1 +'</table>\n</div >\n<div class="tabbertab" style="background: #DDE;border: 1px solid #778;margin-left: 3px;color: #778;"> <h5 >Link</h5>\n<table>'
	                               kml1 = kml1 + '<tr> <td style="font-weight:bold;font-family: Trebuchet MS;font-size:7pt;text-decoration: none;">  ' + str(campo) + '</td><td style="font-family: Trebuchet MS;font-size:7pt;text-decoration: none;">' + str(valore) + ' </td></tr>\n'
	                               if conta_url == 2 :
	                                    kml1 = kml1 +'</table>\n</div > \n'
                         i = i +1 
                       kml1 = kml1 +  '</div >\n</form>\n</body>'     
                  else:
                     kml1 = kml1 + ('<body \n</body>%s %s\n') %( gdxtabella, gid )

                  kml1 = kml1 + ('  ]]></description>\n'   
                     ' <Style>\n'
                     '  <BalloonStyle>\n' 
                     '  <textColor>ff000000</textColor>\n' 
                     '  <displayMode>default</displayMode>\n' 
                     '  <bgColor>2878FAB4</bgColor>\n' 
                     '  </BalloonStyle>\n' 
                     '  </Style>\n'


                     '  %s \n'

                     ' </Placemark>\n'

                     ) %( kml_geo )
            
               else :
               
                  db.close()
                  return kml1                              
            
        db.close()
        return kml1


def completa(x_min, y_min, x_max, y_max, kml1, features, tabella, idfea): 
        geoxmin="7.27"
        geoymin="35.92"
        geoxmax="17.12"
        geoymax="47.09"

        
#CONNESSIONE AL DATABASE            
        db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)
        
        my_user = {"x_min":x_min,"x_max":x_max,"y_min":y_min,"y_max":y_max,"geoxmin":geoxmin,"geoymin":geoymin,"geoxmax":geoxmax,"geoymax":geoymax,"tabella":tabella,"idfea":idfea}


        riga_query = "SELECT  descrizione, lod_min, lod_max  FROM gdx_features where nome = \'%s\' and tabella = \'%s\' and idfea=  \'%s\'"  %(features,tabella,idfea)
        
        a= db.query(riga_query)
        if len(a.dictresult()) > 0:
              for line in a.dictresult():
                     if line['descrizione'] == None:
                        descrizione = tabella + "_" + features + "_" + str(idfea)
                     else:
                        descrizione = line['descrizione']
                     kml1 = kml1 +  ('<NetworkLink>\n'
                         '<name>%s</name>\n') %(descrizione) 

                     if line['lod_min'] == None:
                        lod_min = "128"
                     else:
                        lod_min = line['lod_min']

                     if line['lod_max'] == None:
                        lod_max = "-1"
                     else:
                        lod_max = line['lod_max']


                     
                     kml1 = kml1 +  ('<visibility>0</visibility>\n'	                       
                       '<Region>\n'
                       '<Lod>\n'
                       '<minLodPixels>%s</minLodPixels>\n'
                       '<maxLodPixels>%s</maxLodPixels>\n'
                       '</Lod>\n'
                       '<LatLonAltBox>\n'
                       '   <west>%s</west>\n'	                       
                       '   <south>%s</south>\n'
                       '   <east>%s</east>\n'
                       '   <north>%s</north>\n'
                       '</LatLonAltBox>\n'
                       '</Region>\n'
                       '<Link>\n') %(lod_min,lod_max,geoxmin,geoymin,geoxmax,geoymax)
                     
                     kml1 = kml1 + ('<href>http://%s/htdocs/python/gdx/gdxLayer2kml.%s?LAYERS=%s&amp;FEATURES=%s&amp;IDFEA=%s</href>\n') %(server,pyexe,tabella,features,idfea)                       
                         
                     kml1 = kml1 +  ('<viewRefreshMode>onStop</viewRefreshMode>\n'
                       '<viewRefreshTime>0</viewRefreshTime>\n'	                       
                       '</Link>\n'
                       '</NetworkLink>\n'
                         )  
                              

        db.close()
        return kml1

def maino(x_min, y_min, x_max, y_max, kml1, features): 

        
        geoxmin="7.27"
        geoymin="35.92"
        geoxmax="17.12"
        geoymax="47.09"
        
        idfea = 0
#        descrizione = ''
        
#CONNESSIONE AL DATABASE            
        db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)
        
        my_user = {"x_min":x_min,"x_max":x_max,"y_min":y_min,"y_max":y_max,"geoxmin":geoxmin,"geoymin":geoymin,"geoxmax":geoxmax,"geoymax":geoymax}

# SELECT f_table_name, f_geometry_column, "type" FROM geometry_columns where f_table_name like 'gdx%';


        if (features == 'default'):        
           riga_query = 'SELECT f_table_name, 0 as idfea, null as descrizione FROM geometry_columns where f_table_name like \'gdx%\' order by f_table_name '
        else:
           riga_query = 'SELECT tabella as f_table_name, idfea, descrizione, lod_min, lod_max  FROM gdx_features where nome = \'%s\' order by descrizione, tabella ' %(features)
        
        a= db.query(riga_query)
        if len(a.dictresult()) > 0:
              for line in a.dictresult():
                     f_table_name = line['f_table_name']
                     
                     idfea = line['idfea']                       

                     if line['descrizione'] == None:
                        descrizione = f_table_name + "_" + features + "_" + str(idfea)
                     else:
                        descrizione = line['descrizione']

                     if (idfea > 0):
                       kml1 = kml1 +  ('<NetworkLink>\n'
#                        '<name>%s_%s_%s</name>\n') %(f_table_name,features,idfea)
                        '<name>%s</name>\n') %(descrizione)                     
                     else:
                       kml1 = kml1 +  ('<NetworkLink>\n'
                         '<name>%s</name>\n') %(f_table_name) 

                     if line['lod_min'] == None:
                        lod_min = "128"
                     else:
                        lod_min = line['lod_min']

                     if line['lod_max'] == None:
                        lod_max = "-1"
                     else:
                        lod_max = line['lod_max']


                     
                     kml1 = kml1 +  ('<visibility>0</visibility>\n'	                       
                       '<Region>\n'
                       '<Lod>\n'
                       '<minLodPixels>%s</minLodPixels>\n'
                       '<maxLodPixels>%s</maxLodPixels>\n'
                       '</Lod>\n'
                       '<LatLonAltBox>\n'
                       '   <west>%s</west>\n'	                       
                       '   <south>%s</south>\n'
                       '   <east>%s</east>\n'
                       '   <north>%s</north>\n'
                       '</LatLonAltBox>\n'
                       '</Region>\n'
                       '<Link>\n') %(lod_min,lod_max,geoxmin,geoymin,geoxmax,geoymax)
                     
                     if (idfea > 0):
                        kml1 = kml1 + ('<href>http://%s/htdocs/python/gdx/gdxLayer2kml.%s?LAYERS=%s&amp;FEATURES=%s&amp;IDFEA=%s</href>\n') %(server,pyexe,f_table_name,features,idfea)
                     else:
                        kml1 = kml1 + ('<href>http://%s/htdocs/python/gdx/gdxLayer2kml.%s?LAYERS=%s</href>\n') %(server,pyexe,f_table_name)                       
                         
                     kml1 = kml1 +  ('<viewRefreshMode>onStop</viewRefreshMode>\n'
                       '<viewRefreshTime>0</viewRefreshTime>\n'	                       
                       '</Link>\n'
                       '</NetworkLink>\n'
                         )  
                              

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

     features = 'default1'
     if not (url.has_key("FEATURES")) :
        features = 'default1'
     else:
        features = url["FEATURES"].value
        
     if not (url.has_key("IDFEA")) :
        idfea = 0
     else:        
        idfea = url["IDFEA"].value
        
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
     
     flag ='no' 
       
     if not (url.has_key("BBOX")) :
        flag = 'si'
        bbox = '7.27,35.92,17.12,47.09'
     else:        
        bbox = url["BBOX"].value 
#simona   
     if not (url.has_key("application")) :
        application = ''
     else:
        application = url["application"].value 
           
     bbox1 = bbox.split(',')                                                                                                                                                                                                                                                                                                      
   #  x_min = float(bbox1[0])
   #  y_min = float(bbox1[1])
   #  x_max = float(bbox1[2])
   #  y_max = float(bbox1[3])     
     if (float(bbox1[0]) < float(bbox1[2])) :
        x_min = float(bbox1[0])     
        x_max = float(bbox1[2])
     else :
        x_min = float(bbox1[2])
        x_max = float(bbox1[0])        

     if (float(bbox1[1]) < float(bbox1[3])) :
        y_min = float(bbox1[1]) 
        y_max = float(bbox1[3])            
     else :
        y_min = float(bbox1[3])
        y_max = float(bbox1[1])     

# Url di chiamata a questo applicativo senza parametri estrae la lista dei livelli 
#http://server/htdocs/python/gdx/gdxLayer2kml.py?


# Url di chiamata a questo applicativo (con parametro LAYERS= e BBOX= estrae la geometria all'interno della finestra)
#http://server/htdocs/python/gdx/gdxLayer2kml.py?LAYERS=latina&BBOX=13.44580165497192,41.15829280839811,13.6657960209164,41.27793601092386
     kml =  ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
             '<Document>\n')
     kml1=""
     if (layers == 'ricerca') :
        kml = kml +('<Folder>\n'
                    '<name>LayerList</name>\n')
        app = maino(x_min, y_min, x_max, y_max, kml1, features)
        kml = kml + app + '</Folder>\n'         
     elif (flag == 'si'  ):
         app = completa(x_min, y_min, x_max, y_max, kml1, features,layers,idfea)
         kml = kml + app   #+ '</Folder>\n'
     else :
        app = ""
        kml = kml +('	<Style id="BLU">\n'
			              '		<LineStyle>\n'
			              '			<color>ff8c8c8c</color>\n'
			              '			<width>1</width>\n'
			              '		</LineStyle>\n'
			              '		<PolyStyle>\n'
			              '			<color>7FFF0000</color>\n'
			              '		</PolyStyle>\n'
			              '		<BalloonStyle>\n'
			              '			<text>$[description]</text>\n'
			              '			<color>ffaaaaaa</color>\n'
			              '		</BalloonStyle>\n'
			              '	</Style>\n')	

        kml1=""        
        app = disegna(layers, x_min,y_min,x_max,y_max, kml1, features, idfea)
        kml = kml + app + '</Folder>\n'
     kml = kml  + '</Document>\n'     
     kml = kml + '</kml>\n'           
     try: # Windows only
          import msvcrt
          msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
     except ImportError: pass     
     HEADERS = '\r\n'.join(
       [
        "Content-type: %s",
        "Content-Disposition: attachment; filename=%s",
        "Content-Title: %s",
        "Content-Length: %i",
        "\r\n", # empty line to end headers
        ]
        )
     b = cStringIO.StringIO()
     z = zipfile.ZipFile(b, "w")
     now = time.localtime(time.time())[:6]
     info = zipfile.ZipInfo("doc.kml")
     info.date_time = now
     info.compress_type = zipfile.ZIP_DEFLATED
     z.writestr(info, kml)
     z.close()
      
     output = b.getvalue()  #prende il contenuto dello zip
     length = b.tell()  #memorizza la lunghezza
     b.seek(0)
     if layers <> 'ricerca':
        fileZip = layers
     else:
        fileZip = features  # + ".kmz"
#     sys.stdout.write( HEADERS % ('application/vnd.google-earth.kmz', 'Comtest.kmz', 'Comtest.kmz', length))
     sys.stdout.write( HEADERS % ('application/vnd.google-earth.kmz', fileZip, fileZip, length))
     sys.stdout.write(output)
     b.close()

