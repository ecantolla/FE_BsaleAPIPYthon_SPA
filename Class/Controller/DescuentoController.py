from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DescuentoController:
    def __init__(self):
        self.table=tablas["descuento"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('OLD_API_URL_BASE') + '/discounts.json?limit=50&offset=0'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('OLD_API_KEY')}
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
        query=f"""INSERT INTO {self.table}
                ([id]
                ,[name]
                ,[percentage]
                ,[state]
                ,[automatic])
            VALUES"""
        for current in self.datas:
            query=query+f"""
            ({current["id"]}
           ,'{current["name"]}'
           ,{current["percentage"]}
           ,{current["state"]}
           ,{current["automatic"]}),"""

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
        print("Limpiando descuentos")
        self.executeQuery(self.cleanData())
        print("Obteniendo descuento")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)