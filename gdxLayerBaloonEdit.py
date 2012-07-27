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

#server = 'localhost'

def maino(tabella, gid, htm1): 
       
#CONNESSIONE AL DATABASE            
        db=pg.connect(service, 'localhost', 5432, None, None, uid, pwd)
        
        my_user = {"tabella":tabella, "gid":gid}
        
        
        if (tabella.islower() == False) :
           riga_query = 'SELECT * from "%(tabella)s" where gid = %(gid)s '  %my_user
        else :
           riga_query = "SELECT * from %(tabella)s where gid = %(gid)s "  %my_user
        
        qresult= db.query(riga_query)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        listOfResults = qresult.getresult()
        listOfFields  = qresult.listfields()

        htm1 = htm1 + '<span style="font-weight: bold;">' + str(tabella) + '</span><BR>\n'
        
        i = 0                          
        quanti = qresult.ntuples()  

        for campo in listOfFields:
          for line in listOfResults:
          
             if (str(campo) != "the_geom"): 
                valore = line[i]
                
                if (str(campo) == "gid"):
                   htm1 = htm1 + '<br>' + str(campo) + ': <input type="text" value="' + str(valore) + '"></input>\n'
                else:
                   htm1 = htm1 + '<br>' + str(campo) + ': <input type="text" name="' + str(campo) + '" value="' + str(valore) + '"></input>\n'
               
             i = i +1 
                                                                                                                                                                                                                                                                                                                                 
        db.close()
                                                                                                                                                                                                                                                                                                                    
        return htm1                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                                                                                                                 
if __name__ == "__main__":                                                                                                                                                                                                                                                                                                       
     url = cgi.FieldStorage() 

     action = 'None'
     if not (url.has_key("ACTION")) :
        action = 'None'
     else:        
        action = url["ACTION"].value


     tabella = url["tabella"].value                                                                                                                                                                                                                                                                                                         
     gid  = url["gid"].value                                                                                                                                                                                                                                                                                                    

     print 'Content-Type: text/html\n'
     
     htm = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n'
        '<html>\n'
        '<head>\n'
        '<link rel="stylesheet" href="example.css" type="text/css" media="screen"></head>\n'
          
        '<BODY>EDIT - \n'
                       
        '<form enctype="multipart/form-data" name="formData" method="get|post" action="http://%s/htdocs/python/gdx/gdxLayerRecordUpdate.py">\n'
        '<input type="hidden" name="tabella" value="%s"></input>\n'
        '<input type="hidden" name="gid" value="%s"></input>\n'
         
        '<input value="AGGIORNA" type="submit"> </input>\n'
                ) %(server, tabella, gid)

           
            
     htm1=""
     app = maino(tabella, gid, htm1)

     htm = htm + app
 
     htm = htm  + '</form></BODY>\n' 
     htm = htm  + '</HTML>\n' 
     print  htm
                                     
                                           

