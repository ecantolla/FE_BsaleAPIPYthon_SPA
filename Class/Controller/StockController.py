from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class StockController:
    def __init__(self):
        self.table=tablas["stock"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/stocks.json?limit=50&offset=0'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            print(url)
            if("next" in response):
                flag=True
                url=response["next"]+''
            else:
                flag=False
            for current in response["items"]:
                self.datas.append(current)
    def getInsertQuery(self):
        query=f"""INSERT INTO {self.table}
                ([quantity]
                ,[quantityReserved]
                ,[quantityAvailable]
                ,[idVariante]
                ,[idSucursal])
            VALUES"""
        i=0
        for current in self.datas:
            i=i+1
            query=query+f"""
                ({current["quantity"]}
                ,{current["quantityReserved"]}
                ,{current["quantityAvailable"]}
                ,{current["variant"]["id"]}
                ,{current["office"]["id"]}),"""
            if i>900:
                i=0
                print("insertando 900 stocks")
                query=query.replace("'None'",'null')
                query=query[:-1]
                self.executeQuery(query)
                query=f"""INSERT INTO {self.table}
                    ([quantity]
                    ,[quantityReserved]
                    ,[quantityAvailable]
                    ,[idVariante]
                    ,[idSucursal])
                VALUES"""

        query=query.replace("'None'",'null')
        query=query[:-1]
        self.executeQuery(query)
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando stock")
        self.executeQuery(self.cleanData())
        print("Obteniendo stock")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        #self.executeQuery(query)
