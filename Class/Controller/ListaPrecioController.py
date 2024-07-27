from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ListaPrecioController:
    def __init__(self):
        self.table=tablas["listaPrecio"]
        self.datas=[]
        self.detalle=tablas["detalleListaPrecio"]

    def cleanData(self):
        query=f"""delete from {self.table}"""
        self.executeQuery("delete from "+self.detalle)
        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/price_lists.json?limit=50&expand=[coin,details]'
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
        query=f"""INSERT INTO {self.table}
                ([id]
                ,[name]
                ,[description]
                ,[state]
                ,[details])
            VALUES"""
        for current in self.datas:
            query=query+f"""
            ({current["id"]}
           ,'{current["name"]}'
           ,'{current["description"]}'
           ,{current["state"]}
           ,'{current["details"]["href"]}'),"""
            detailsQuery=f"""
                INSERT INTO {self.detalle}
                    ([id]
                    ,[variantValue]
                    ,[variantValueWithTaxes]
                    ,[idVariante]
                    ,[idListaPrecio])
                VALUES
                """
            for detail in current["details"]["items"]:
                detailsQuery=detailsQuery+f"""
                    ({detail["id"]}
                        ,{detail["variantValue"]}
                        ,{detail["variantValueWithTaxes"]}
                        ,{detail["variant"]["id"]}
                        ,{current["id"]}),"""
            detailsQuery=detailsQuery[:-1]
            self.executeQuery(detailsQuery)        
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
