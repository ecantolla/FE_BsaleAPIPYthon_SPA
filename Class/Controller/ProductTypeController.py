from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ProductTypeController:
    def __init__(self):
        self.table=tablas["tipoProducto"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('OLD_API_URL_BASE') + '/product_types.json?limit=50&expand=[attributes]'
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
        atributoTable=tablas["atributo"]
        atributoQuery="delete from "+atributoTable
        self.executeQuery(atributoQuery)
        query=f"""INSERT INTO {self.table}
            ([id]
           ,[name]
           ,[isEditable]
           ,[state]
           ,[imagestionCategoryId]
           ,[prestashopCategoryId]
           ,[attributos])
            VALUES"""
        for current in self.datas:
            query=query+f"""
                ({current["id"]}
                ,'{current["name"]}'
                ,{current["isEditable"]}
                ,{current["state"]}
                ,{current["imagestionCategoryId"]}
                ,{current["prestashopCategoryId"]}
                ,'{current["attributes"]["href"]}'),"""
            
            if len(current["attributes"]["items"]) >0:                
                atributoQuery=f"""
                        INSERT INTO {atributoTable}
                        ([id]
                        ,[name]
                        ,[isMandatory]
                        ,[generateVariantName]
                        ,[hasOptions]
                        ,[options]
                        ,[state]
                        ,[idTipoProducto])
                        VALUES
                        """
                for att in current["attributes"]["items"]:
                    options = att.get("options", "")  # Use a default empty string if att["options"] is missing
                    if isinstance(options, str):
                        options = options.replace('|', '')  # Now you can safely replace '|'
                    else:
                        options = ""  # Set options to an empty string if it's not a string
                    
                    atributoQuery=atributoQuery+f"""
                        ({att["id"]}
                        ,'{att["name"]}'
                        ,{att["isMandatory"]}
                        ,{att["generateVariantName"]}
                        ,{att["hasOptions"]}
                        ,'{options}'
                        ,{att["state"]}
                        ,{current["id"]}),"""
                atributoQuery=atributoQuery[:-1]
                
                self.executeQuery(atributoQuery)
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
        print("Limpiando tipo documento")
        self.executeQuery(self.cleanData())
        print("Obteniendo tipo documento")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)