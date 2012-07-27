httpd.conf

"	inserire la seguente riga per mod_python
LoadModule python_module modules/mod_python.so
Installazione su http://www.modpython.org/ (python 2.5 apache 2.0)
"	Abilitare la modalità CGI
<Directory />    
    AllowOverride None
   # Options FollowSymLinks  + ExecCGI
    Order allow,deny 
    Allow from all 
</Directory>
"	Abilitare il mod_python
<Directory "c:/ms4w/Apache/htdocs/python/gdx">   
   AddHandler mod_python .psp
    PythonHandler mod_python .psp
    PythonDebug On
</Directory> 
"	Gestione dei file kmz
AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddType application/vnd.google-earth.kml+xml kml
    AddType application/vnd.google-earth.kmz kmz
"	Gestione dei python e cgi
  AddHandler cgi-script .cgi  .py   .pyc    .gdx
    AddHandler server-parsed .html

Python e directory
Tutte le directory  e file python devono essere copiati nella directory Apache/htdocs/python/gdx
css
Images
Javascript
Thumbs
_gdxvars.py contiene  i dati di connessione (userid,password,server,nome schema)
gdx_features_iwk.py  legge dal database i layer pubblicabili e restituisce una pagina html
gdxLayer2kml.py legge dal database e trasforma il layer in kmz
gdxLayerBalNone.py  invia la richiesta al server per richiedere i dati alfanumerici del poligono selezionato
gdxLayerBaloonEdit.py invia la richiesta al server per aggiornare i dati alfanumerici del poligono 
selezionato
gdxLayerRecordUpdate.py aggiorna la base dati
Dump postgis2_copy 
Contiene lo schema delle tabelle necessario per il funzionamento del sistema


