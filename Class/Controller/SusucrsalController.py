from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json

class SucursalController:
    def __init__(self):
        self.table=tablas["sucursal"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = 'https://api.bsale.cl/v1/offices.json'
        flag=True
        headers = {'Accept': 'application/json','access_token':'6de4c01b2a3d7f64153f0e4f96b1c1f51218be56'}
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
                ,[description]
                ,[address]
                ,[latitude]
                ,[longitude]
                ,[isVirtual]
                ,[country]
                ,[municipality]
                ,[city]
                ,[zipCode]
                ,[email]
                ,[costCenter]
                ,[state]
                ,[imagestionCellarId]
                ,[defaultPriceList])
            VALUES"""
        for current in self.datas:
            query=query+f"""
                ({current["id"]}
                ,'{current["name"]}'
                ,'{current["description"]}'
                ,'{current["address"]}'
                ,'{current["latitude"]}'
                ,'{current["longitude"]}'
                ,{current["isVirtual"]}
                ,'{current["country"]}'
                ,'{current["municipality"]}'
                ,'{current["city"]}'
                ,'{current["zipCode"]}'
                ,'{current["email"]}'
                ,'{current["costCenter"]}'
                ,{current["state"]}
                ,{current["imagestionCellarId"]}
                ,{current["defaultPriceList"]}),"""

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
        print("Limpiando sucursales")
        self.executeQuery(self.cleanData())
        print("Obteniendo sucursales")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)