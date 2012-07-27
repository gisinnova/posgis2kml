#!c:/ms4w/apps/python25/python.exe
# ################################ version 1.0
#Author: geodrinx@gmail.com; gisinnova@gmail.com
# ################################ version 1.0
#Licensed under MIT License. Read the file LICENSE for more information   *
import cgi
import pg
import os
import sys
import time
import httplib
import string
import _gdxvars
def main(url): 
        pyexe  = _gdxvars.pyexe
        server = 'localhost' #_gdxvars.server
        uid    = _gdxvars.uid
        pwd    = _gdxvars.pwd
        service= _gdxvars.service
        
        tabella = url["tabella"].value    
        gid = url["gid"].value
     

      
        # Connessione al database

        
        db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)

#-----  Prendo la "describe" della tabella

        tipo = ""

        riga_query0 = ("SELECT	a.attname AS campo,	t.typname AS tipo FROM	pg_class c,	pg_attribute a,	pg_type t WHERE	c.relname = '%s'") %(tabella) 

        riga_query0 = riga_query0 + "and a.attnum > 0	and a.attrelid = c.oid	and a.atttypid = t.oid ORDER BY a.attnum"
        
        a0= db.query(riga_query0)
        
        if len(a0.dictresult()) > 0:
           for line in a0.dictresult():

              campo = line['campo']

              if campo != "the_geom" and campo != "gid" :   
                 valore = url[campo].value
                 tipo = line['tipo']                        
                 valore = valore.replace(chr(39),  chr(39)+ chr(39)) 
                 riga_query = 'UPDATE "%s" SET "%s" = ' %(tabella, campo)

                 if (valore == "None"):
                    valore = "Null"
                    riga_query = riga_query + "%s WHERE gid = %s" %( valore, gid)
                 else:   
                    if ( tipo == "varchar" or tipo == "bpchar" or tipo == "text"):
                       riga_query = riga_query + "rtrim('%s') WHERE gid = %s" %(valore, gid)
                    else:
                       riga_query = riga_query + "%s WHERE gid = %s" %( valore, gid)                 
        
                 a= db.query(riga_query)


        db.close()
        return gid
        
              

if __name__ == "__main__":
     url = cgi.FieldStorage()

     tabella = url["tabella"].value    
     gid = url["gid"].value
     
           
     app = main(url) 
     html = ( 
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
        '<html>\n'
        '<head>\n'
        '  <meta content="text/html; charset=ISO-8859-1"\n'
        ' http-equiv="content-type">\n'
        '  <title>AGGIORNAMENTO EFFETTUATO!</title>\n'
        '</head>\n'
        '<body>\n'
        '<br>AGGIORNAMENTO EFFETTUATO!<br> tabella: %s<br> gid: %s\n'
        '</body>\n'
        '</html>\n'
        ) %(tabella, gid)
     print 'Content-Type: text/html\n'
     print html
