#!c:/ms4w/apps/python25/python.exe
# ################################ version 1.0
#Author: geodrinx@gmail.com; gisinnova@gmail.com
# ################################ version 1.0
#Licensed under MIT License. Read the file LICENSE for more information   *
#    postgres version 8.4.2
# Read gdx_features table (metadata table) and make the kmz catalogue 
#   desc gdx_features
#   idfea integer NOT NULL,            ** key
#   idcat integer,                              **category
#   nome character varying,            **name theme
#   tabella character varying,          **name table
#   graphics character varying,       ** style (color, symbol etc)
#   azione character varying,          ** python file balloon action (view,insert,update)
#   condizione character varying,   ** filter table
#   descrizione character varying,  ** label theme
#   tooltips character varying,        ** label content
#   extrusion character varying,     ** extrude theme
#   descrfeature character varying,** 
#   lod_min character varying,       ** scale min
#   lod_max character varying,      ** scale max
#   timeout character varying        ** timeout downloads 
#
#
#
#################################
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


#pyexe  = 'py' # _gdxvars.pyexe
#server = 'localhost' #_gdxvars.server
#uid    = "postgres"#_gdxvars.uid
#pwd    = "postgres"#_gdxvars.pwd
#service= "postgis2_copy"#_gdxvars.service

def listaLayersByFeature(featureName):
     db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)
     riga_query0 = ("SELECT * from gdx_features where nome = '%s' order by descrizione,idfea") %(featureName) 
     kml1 = ""         
                    
     a0 = db.query(riga_query0)
     if len(a0.dictresult()) > 0:

        for line in a0.dictresult():

           if line == None:
              idfea = ""
           else:
              idfea = line['idfea']

           if line == None:
              idcat = ""
           else:
              idcat = line['idcat']

           if line == None:
              nome = ""
           else:
              nome = line['nome']
              
           if line == None:
              tabella = ""
           else:
              tabella = line['tabella']

           if line == None:
              graphics = ""
           else:
              graphics = line['graphics']
              
           if line == None:
              azione = ""
           else:
              azione = line['azione']

           if line == None:
              condizione = ""
           else:
              condizione = line['condizione']
              
           if line == None:
              descrizione = ""
           else:
              descrizione = line['descrizione']

           if line == None:
              tooltips = ""
           else:
              tooltips = line['tooltips']
              
           if line == None:
              extrusion = ""
           else:
              extrusion = line['extrusion']                                                                      

 #          kml1 = kml1 +  ('<ul class="pageitem"><li class="textbox"><span class="header">Nome:  <strong>      %s</strong></span><p>') %(nome)
#          kml1 = kml1 +  ('<BR>IDCAT:       %s') %(idcat)
           if (tabella > 0):
             kml1 = kml1 +  ('<br>Layers:<a href="http://%s/htdocs/python/gdx/gdxLayer2kml.%s?FEATURES=%s">%s</a>\n') %(server, pyexe, featureName, featureName) 
             kml1 = kml1 +  ('<ul class="pageitem"><li class="textbox"><span class="header"><strong> %s</strong><a href="http://%s/htdocs/python/gdx/gdxLayer2kml.%s?LAYERS=%s&FEATURES=%s&IDFEA=%s"&nbsp&nbsp&nbsp> <img alt="visualizza con google earth" src="thumbs/google.png" /> KMZ</a></span><p>') %(descrizione,server,pyexe,tabella,nome,idfea)
             kml1 = kml1 +  ('<ul class="pageitem"><li class="textbox"><span class="header">Tabella:        %s</span><p>') %(tabella)
             kml1 = kml1 +  ('<strong>IDfea:</strong>  %s') %(idfea)  
			#	kml1 = kml1 +  ('<BR>Graphics:    %s') %(graphics)
			#	kml1 = kml1 +  ('<BR>Azione:      %s') %(azione)
             if (condizione != None):
               kml1 = kml1 +  ('<BR><strong>Condizione:</strong>  %s') %(condizione)
             if (tooltips != None):  
               kml1 = kml1 +  ('<BR><strong>Tooltips:</strong>    %s') %(tooltips)
			#	kml1 = kml1 +  ('<BR>Extrusion:   %s') %(extrusion)
             kml1 = kml1 +  ('<BR><strong>Url:</strong>   http://%s/htdocs/python/gdx/gdxLayer2kml.%s?LAYERS=%s&FEATURES=%s&IDFEA=%s') %(server,pyexe,tabella,nome,idfea)
             kml1 = kml1 +  ('</p></li> </ul></p></li> </ul> \n')
           else:   
             kml1 = kml1 +  ('<br>Layers: %s\n') %( featureName) 
                
     db.close()
     return kml1


def listaFeatures():

     kml1 = ""
     db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)
     riga_query0 = "SELECT distinct nome, descrfeature FROM gdx_features where descrfeature is not null order by nome"

     a0 = db.query(riga_query0)

     if len(a0.dictresult()) > 0:
        for line in a0.dictresult():
           if line == None:
              nome = ""
           else:
              nome = line['nome']
              
           if line == None:
              descrfeature = ""
           else:
              descrfeature = line['descrfeature']              
           kml1 = kml1 +  ('<li class="menu"><span class="name"><a href="http://%s/htdocs/python/gdx/gdx_features_iwk.py?nome=%s">%s</a><img alt="visualizza con google earth" src="thumbs/google.jpg" /></span>') %(server,nome, nome)             
           kml1 = kml1 +  ('<span class="comment"> %s </span><span class="arrow"></span></li>\n') %(descrfeature) 
     db.close()
     return kml1

if __name__ == "__main__":
     ritorno = "/htdocs/python/gdx/"
     url = cgi.FieldStorage()
     html = ""
     html = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
     '<html xmlns="http://www.w3.org/1999/xhtml">'
        '<html>\n'
        '<head>\n'
        '  <meta content="text/html; charset=ISO-8859-1"\n'
        ' http-equiv="content-type">\n'
        '<meta content="yes" name="apple-mobile-web-app-capable" />'
        '<meta content="index,follow" name="robots" />'
        '<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />'
        '<link href="pics/homescreen.gif" rel="apple-touch-icon" />'
        '<meta content="minimum-scale=1.0, width=device-width, maximum-scale=0.6667, user-scalable=no" name="viewport" />'
        '<link href="css/style.css" rel="stylesheet" media="screen" type="text/css" />'
        '<script src="javascript/functions.js" type="text/javascript"></script>'
        '<title>INNOVA : Lista layers</title>'
       '<link href="pics/startup.png" rel="apple-touch-startup-image" />'
        '<meta content="iPod,iPhone,Webkit,iWebkit,Website,Create,mobile,Tutorial,free" name="keywords" />'
        '<meta content="Try out all the new features of iWebKit 5 with a simple touch of a finger and a smooth screen rotation!" name="description" />'
        '</head>\n'
        '<body>\n'
        '<div id="topbar">'
        '<div id="title">INNOVA <img alt="home" src="thumbs/favicon.ico" /> </div>')
        
     if not (url.has_key("nome")) :
        nome = '-'
        span = (
                  '<div class="searchbox"> '
	              '<form action="" method="get"> '
		          '<fieldset><input id="search" placeholder="search" type="text"  name="cerca" />' 
		          '<input id="submit" type="hidden" /></fieldset> '
	              '</form>' 
                  '</div><span class="graytitle">Elenco Features</span>')
        html= html + ( '<div id="rightnav">'
                  '<a href='+  ritorno + 'gdx_crea_feature_iwk.py >Nuova feature</a>'
                  '</div>'
                  '</div>'
                  '<div id="content">')
      #  html = html + ( '<div id="duoselectionbuttons">'
      #  '<a href=' +  ritorno + 'gdx_crea_feature_iwk.py >+ features</a>'
     #    '<a href="page.html" >- features</a>'
       
    #    '</div>')
     else:        
        nome = url["nome"].value
        span =''
        html = html + ('</div><div id="leftnav">'
        '<a href="' +  ritorno + 'gdx_features_iwk.py" >Elenco Features</a>'
        '</div>'
        
         '<div id="tributton">'
        '<div class="links"> '
		'<a id="pressed" href="' +  ritorno + 'gdx_crea_tabella_iwk.py?nomel=' + nome +'">aggiungi</a><a href="resume.html">elimina</a><a href="portfolio.html">accoda</a></div> '
        '</div><div id="content">')
    
     html = html + span +(
     	'<ul class="pageitem">'
	'	<li class="textbox"><p>'
        )
      
     if (nome == "-") :   
        app = listaFeatures() 
     else :
     
     # entro per nome features impostato          
        app = listaLayersByFeature(nome)

     html = html + app        
        
     html =  html + (   '</body>\n'
        '</html>\n'
        )       
     print 'Content-Type: text/html\n'
     
     print html
