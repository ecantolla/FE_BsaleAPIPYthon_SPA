from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ProductController:
    def __init__(self):
        self.table=tablas["producto"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('OLD_API_URL_BASE') + '/products.json?limit=50&expand=[product_type]'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('OLD_API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            if("next" in response):
                flag=True
                url=response["next"]+'&expand=[product_type]'
            else:
                flag=False
            for current in response["items"]:
                self.datas.append(current)
    def getInsertQuery(self):
        query = f"""INSERT INTO {self.table}
           ([id]
           ,[name]
           ,[description]
           ,[classification]
           ,[ledgerAccount]
           ,[allowDecimal]
           ,[stockControl]
           ,[printDetailPack]
           ,[state]
           ,[prestashopProductId]
           ,[presashopAttributeId]
           ,[idTipoProducto])
            VALUES"""


        product_types = {}  # Store unique product type data

        i = 0
        for current in self.datas:
            i += 1
            query += f"""
                ({current["id"]}
                ,'{current.get("name", "")}'  -- Handle NULL or missing name
                ,'{current.get("description", "")}'  -- Handle NULL or missing description
                ,{current.get("classification", 0)}  -- Handle NULL or missing classification
                ,'{current.get("ledgerAccount", 0)}'  -- Handle NULL or missing ledgerAccount
                ,{current.get("allowDecimal", 0)}  -- Handle NULL or missing allowDecimal
                ,{current.get("stockControl", 0)}  -- Handle NULL or missing stockControl
                ,{current.get("printDetailPack", 0)}  -- Handle NULL or missing printDetailPack
                ,{current.get("state", 0)}  -- Handle NULL or missing state
                ,{current.get("prestashopProductId", 0)}  -- Handle NULL or missing prestashopProductId
                ,{current.get("presashopAttributeId", 0)}  -- Handle NULL or missing presashopAttributeId
                ,'{current["product_type"]["id"]}'),"""

            type_data = current["product_type"]
            product_type_id = type_data["id"]
            if product_type_id not in product_types:
                # If product type is not in the dictionary, add it
                product_types[product_type_id] = type_data

            if i > 900:
                i = 0
                print("inserting 900 products")
                query = query.replace("'None'", 'null')
                query = query[:-1]
                self.executeQuery(query)
                query = f"""INSERT INTO {self.table}
                       ([id]
                       ,[name]
                       ,[description]
                       ,[classification]
                       ,[ledgerAccount]
                       ,[allowDecimal]
                       ,[stockControl]
                       ,[printDetailPack]
                       ,[state]
                       ,[prestashopProductId]
                       ,[presashopAttributeId]
                       ,[idTipoProducto])
                        VALUES"""
        query = query.replace("'None'", 'null')
        query = query[:-1]

        product_query = query
        return product_query,product_types
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando products")
        self.executeQuery(self.cleanData())
        print("Obteniendo products")
        self.getData()
        print("Generando Query")
        product_query, product_types = self.getInsertQuery()
        print("Termino query de producto")

        print("Iniciando query de tipo de producto")
        # Execute product data insertion
        self.executeQuery(product_query)


        # Execute type data insertion for each unique product type
        for product_type_id, type_data in product_types.items():

            single_type_query = f"""MERGE INTO {tablas["tipoProducto"]} AS Target
                USING (VALUES (
                    {product_type_id},
                    '{type_data.get("name", "")}',
                    {type_data.get("isEditable", 0)},
                    {type_data.get("state", 0)},
                    {type_data.get("imagestionCategoryId", 0)},
                    {type_data.get("prestashopCategoryId", 0)},
                    '{type_data["attributes"]["href"]}'
                )) AS Source (id, name, isEditable, state, imagestionCategoryId, prestashopCategoryId, attributos)
                ON Target.id = Source.id
                WHEN MATCHED THEN
                    UPDATE SET
                        name = Source.name,
                        isEditable = Source.isEditable,
                        state = Source.state,
                        imagestionCategoryId = Source.imagestionCategoryId,
                        prestashopCategoryId = Source.prestashopCategoryId,
                        attributos = Source.attributos
                WHEN NOT MATCHED THEN
                    INSERT (id, name, isEditable, state, imagestionCategoryId, prestashopCategoryId, attributos)
                    VALUES (Source.id, Source.name, Source.isEditable, Source.state, Source.imagestionCategoryId, Source.prestashopCategoryId, Source.attributos);"""

            self.executeQuery(single_type_query)
        print("Termino query de tipo de producto en base a productos")
