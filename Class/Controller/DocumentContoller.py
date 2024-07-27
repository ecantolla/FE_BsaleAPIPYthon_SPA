from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
from Class.Models.Document import Document
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentController:
    def __init__(self,firstDay,lastDay) -> None:
        self.lastDay=lastDay
        self.firstDay=firstDay

    def process(self):
        #eliminar llos documentos existentes
        con=ConnectionHandler()
        con.connect()
        deleteQuery=self.getDeleteQuery()
        con.executeQuery(deleteQuery)
        con.commitChange()
        print("Eliminados los documentos")
        acumulados=50
        url = os.getenv('API_URL_BASE') + '/documents.json?expand=details,sellers,attributes&emissiondaterange=['+str(self.firstDay)+','+ str(self.lastDay)+']&offset='+str(acumulados)+"&limit=50"
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            acumulados=acumulados+len(response["items"])
            if("next" in response):
                flag=True
                url = os.getenv('API_URL_BASE') + '/documents.json?expand=details,sellers,attributes&emissiondaterange=['+str(self.firstDay)+','+ str(self.lastDay)+']&offset='+str(acumulados)+"&limit=50"
            else:
                flag=False
            #procesar las solicitudes 
            for current in response["items"]:
                deleteQuery=self.getDeleteQueryDetail(current["id"])
                con.executeQuery(deleteQuery)
                con.commitChange()
                for detail in current["details"]["items"]:
                    print("")
    def getDeleteQuery(self):
        return "delete from "+tablas["documento"]+" where emissionDate between "+str(self.firstDay)+" and "+str(self.lastDay)

    def getDeleteQueryDetail(self,id):
        return "delete from "+tablas["detalleDocumento"]+" where idDocumento="+str(id)
