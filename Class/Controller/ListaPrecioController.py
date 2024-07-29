from Class.Controller.AbstractController import AbstractController
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ListaPrecioController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.table2 = tablas["detalleListaPrecio"]

    def get_data(self):
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
                INSERT INTO {self.table2}
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

    def executelogic(self):
        print("Limpiando ")
        self.clear_table()
        self.clear_table(self.table2)
        print("Obteniendo descuento")
        self.get_data()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)
