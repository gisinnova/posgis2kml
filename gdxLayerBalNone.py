#!c:/ms4w/apps/python25/python.exe
# ################################ version 1.0
#Author: geodrinx@gmail.com; gisinnova@gmail.com
# ################################ version 1.0
#Licensed under MIT License. Read the file LICENSE for more information   *
import cgi
import pg
import string
import _gdxvars
pyexe  = _gdxvars.pyexe
server = 'localhost' #_gdxvars.server
uid    = _gdxvars.uid
pwd    = _gdxvars.pwd
service= _gdxvars.service
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                 
if __name__ == "__main__":                                                                                                                                                                                                                                                                                                       
     url = cgi.FieldStorage() 

     tabella = url["tabella"].value                                                                                                                                                                                                                                                                                                         
     numero  = url["numero"].value                                                                                                                                                                                                                                                                                                    

     print 'Content-Type: text/html\n'
     
     htm = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
        '<html>\n'
        '<head>\n'
        '</head>\n'
        '<BODY>\n'        
        '<span style="font-weight: bold;">NESSUN DATO VISIBILE</span><BR>\n')           
            
 
     htm = htm  + '</BODY>\n' 
     htm = htm  + '</HTML>\n' 
     print  htm
                                     
                                           

