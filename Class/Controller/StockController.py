from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json

class StockController:
    def __init__(self):
        self.table=tablas["stock"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = 'https://api.bsale.cl/v1/stocks.json?limit=50&offset=0'
        flag=True
        headers = {'Accept': 'application/json','access_token':'6de4c01b2a3d7f64153f0e4f96b1c1f51218be56'}
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