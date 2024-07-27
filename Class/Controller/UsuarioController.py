from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class UsuarioController:
    def __init__(self):
        self.table=tablas["usuario"]
        self.datas=[]
        self.offset=0
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/users.json?limit=50&offset='+str(self.offset)
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            if("next" in response):
                flag=True
                url=response["next"]+''
            else:
                flag=False
            for current in response["items"]:
                
                self.datas.append(current)
    def getInsertQuery(self):
        query=f"""
            INSERT INTO {self.table}
                ([id]
                ,[firstName]
                ,[lastName]
                ,[email]
                ,[state]
                ,[idSucursal])
            VALUES
        """
        for current in self.datas:
            query=query+ f"""
                ({current["id"]}
                ,'{current["firstName"]}'
                ,'{current["lastName"]}'
                ,'{current["email"]}'
                ,{current["state"]}
                ,{current["office"]["id"]}),"""
        query=query.replace("'None'",'null')
        query=query[:-1]
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando Usuario")
        self.executeQuery(self.cleanData())
        print("Obteniendo usuarios")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)
