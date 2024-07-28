from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import *
import requests
import json
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class VarianteController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        
        self.productTable = tablas["producto"]
        c_pt = np.array([ct for ct in get_col_dtype(self.productTable)])
        self.p_cols = c_pt[:, 0].tolist()
        self.pc_types = c_pt[:, 1].tolist()
        self.data_products = []

        self.attTable = tablas["valorAtributo"]
        c_at = np.array([ct for ct in get_col_dtype(self.attTable)])
        self.a_cols = c_at[:, 0].tolist()
        self.ac_types = c_at[:, 1].tolist()
        self.data_attribs = []

    def cleanData(self):
        tablas = [self.table, self.attTable, self.productTable]
        for tabla in tablas:
            self.execute_query(f"TRUNCATE TABLE {tabla}", 'truncate')
    
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/variants.json?expand=[attribute_values,product,costs]&limit=50&offset=0'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        i=0
        while True:
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            
            for current in response["items"]:
                if 'product' in current:
                    current['idProducto'] = current['product']['id']
                if 'attribute_values' in current:
                    current['atributos'] = current['attribute_values']['href']
                if 'costs' in current:
                    current['costos'] = os.getenv('API_URL_BASE') + '/variants/' + str(current['id']) + '/costs.json'
                    if "averageCost" in current["costs"]:
                        current["costoPromedio"] = current["costs"]["averageCost"]

                current['barCode'] = current["barCode"].replace("'","")
                #breakpoint()
                #aqui se inserta en el array de variante
                current_variant = format_record(current, self.cols, self.ctypes)
                self.datas.append(current_variant)

                # aqui insertamos en el array de atributos
                for att in current["attribute_values"]["items"]:
                    att['idVariante'] = current['id']
                    att['idAtributo'] = att['attribute']['id']
                    att['description'] = att['description'].replace("'","''")
                    current_attrib = format_record(att, self.a_cols, self.ac_types)
                    self.data_attribs.append(current_attrib)                

                # aqui insertamos en el array de productos
                if 'product_type' in current['product']:
                    current['product']['idTipoProducto'] = current['product']['product_type']['id']
                current_product = format_record(current['product'], self.p_cols, self.pc_types)
                self.data_products.append(current_product)
                
            if "next" in response['items']:
                url = response["next"] + '&expand=[attribute_values,product,costs]'
            else:
                break

    def getInsertQuery(self):
        query=f"""
        INSERT INTO {self.table}
                ([id]
                ,[description]
                ,[unlimitedStock]
                ,[allowNegativeStock]
                ,[state]
                ,[barCode]
                ,[code]
                ,[imagestionCenterCost]
                ,[imagestionAccount]
                ,[imagestionConceptCod]
                ,[imagestionProyectCod]
                ,[imagestionCategoryCod]
                ,[imagestionProductId]
                ,[serialNumber]
                ,[prestashopCombinationId]
                ,[prestashopValueId]
                ,[idProducto]
                ,[atributos]
                ,[costos]
                ,[costoPromedio])
            VALUES
            """
        products=[]
            
        attQuery=f"""
            INSERT INTO {self.attTable}
                ([id]
                ,[description]
                ,[idAtributo]
                ,[idVariante])
                VALUES
                """
        
        productQuery=f"""
                INSERT INTO {self.productTable}
                    ([id]
                    ,[name]
                    ,[description]
                    ,[classification]
                    ,[ledgerAccount]
                    ,[costCenter]
                    ,[allowDecimal]
                    ,[stockControl]
                    ,[printDetailPack]
                    ,[state]
                    ,[prestashopProductId]
                    ,[presashopAttributeId]
                    ,[idTipoProducto])
                VALUES
                """
        contAtt=0
        contProduct=0
        contVariante=0
        for current in self.datas:
            #eliminar los productos
            contVariante=contVariante+1
            avg=0
            if "costs" in current:
                if "averageCost" in current["costs"]:
                    avg=current["costs"]["averageCost"]
            
            query=query+f"""
                ({current["id"]}
                ,'{current["description"]}'
                ,{current["unlimitedStock"]}
                ,{current["allowNegativeStock"]}
                ,{current["state"]}
                ,'{current["barCode"].replace("'","")}'
                ,'{current["code"]}'
                ,{current["imagestionCenterCost"]}
                ,{current["imagestionAccount"]}
                ,{current["imagestionConceptCod"]}
                ,{current["imagestionProyectCod"]}
                ,{current["imagestionCategoryCod"]}
                ,{current["imagestionProductId"]}
                ,{current["serialNumber"]}
                ,{current["prestashopCombinationId"]}
                ,{current["prestashopValueId"]}
                ,{current["product"]["id"]}
                ,'{current["attribute_values"]["href"]}'
                ,'{os.getenv("API_URL_BASE")}/variants/{current["id"]}/costs.json'
                ,{avg}),"""
            if(contVariante>900):
                contVariante=0
                query=query.replace("'None'",'null')
                query=query[:-1]
                self.executeQuery(query)
                query=f"""
                    INSERT INTO {self.table}
                            ([id]
                            ,[description]
                            ,[unlimitedStock]
                            ,[allowNegativeStock]
                            ,[state]
                            ,[barCode]
                            ,[code]
                            ,[imagestionCenterCost]
                            ,[imagestionAccount]
                            ,[imagestionConceptCod]
                            ,[imagestionProyectCod]
                            ,[imagestionCategoryCod]
                            ,[imagestionProductId]
                            ,[serialNumber]
                            ,[prestashopCombinationId]
                            ,[prestashopValueId]
                            ,[idProducto]
                            ,[atributos]
                            ,[costos]
                            ,[costoPromedio])
                        VALUES
                        """
            #agregar producto
            if current["product"]["id"] not in products:
                products.append(current["product"]["id"])
                contProduct=contProduct+1
                productQuery=productQuery+f"""
                    ({current["product"]["id"]}
                    ,'{current["product"]["name"]}'
                    ,'{current["product"]["description"]}'
                    ,{current["product"]["classification"]}
                    ,'{current["product"]["ledgerAccount"]}'
                    ,'{current["product"]["costCenter"]}'
                    ,{current["product"]["allowDecimal"]}
                    ,{current["product"]["stockControl"]}
                    ,{current["product"]["printDetailPack"]}
                    ,{current["product"]["state"]}
                    ,{current["product"]["prestashopProductId"]}
                    ,{current["product"]["presashopAttributeId"]}
                    ,{current["product"]["product_type"]["id"]}),"""
                if contProduct>900:
                    contProduct=0
                    productQuery=productQuery[:-1]
                    self.executeQuery(productQuery)
                    productQuery=f"""
                        INSERT INTO {self.productTable}
                            ([id]
                            ,[name]
                            ,[description]
                            ,[classification]
                            ,[ledgerAccount]
                            ,[costCenter]
                            ,[allowDecimal]
                            ,[stockControl]
                            ,[printDetailPack]
                            ,[state]
                            ,[prestashopProductId]
                            ,[presashopAttributeId]
                            ,[idTipoProducto])
                        VALUES
                        """            
            #eliminar los atributos
            for att in current["attribute_values"]["items"]:
                contAtt=contAtt+1

                atrdescription = att["description"]
                if atrdescription:
                    atrdescription = atrdescription.replace("'", "''")

                attQuery=attQuery+f"""        
                    ({att["id"]}
                    ,'{atrdescription}'
                    ,{att["attribute"]["id"]}
                    ,{current["id"]}),"""
                if contAtt>900:
                    contAtt=0
                    attQuery=attQuery[:-1]
                    #attQuery=attQuery.replace("L'OREAL","LOREAL")
                    #attQuery=attQuery.replace("L'Oreal","L''Oreal")
                    self.executeQuery(attQuery)
                    attQuery=f"""
                        INSERT INTO {self.attTable}
                            ([id]
                            ,[description]
                            ,[idAtributo]
                            ,[idVariante])
                            VALUES
                            """        
        productQuery=productQuery[:-1]
        print("producto")
        
        self.executeQuery(productQuery)
        #attQuery=attQuery.replace("L'OREAL","LOREAL")
        #attQuery=attQuery.replace("L'Oreal","L''Oreal")
        attQuery=attQuery[:-1]
        print("atributo")
        att=open('Atributos.txt','w')
        att.write(attQuery)
        self.executeQuery(attQuery)
        query=query.replace("'None'",'null')
        query=query[:-1]
        print("variante")
        file=open("test.txt","w")
        file.write(productQuery)
        file.close()
        self.executeQuery(query)
        return query
    def insert_data(self):
        #insert data for varianate table
        query = f'INSERT INTO {self.table} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []

        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 900 == 0:
                print(f"insertando variante {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)

        #insert data for attribute table
        query2 = f'INSERT INTO {self.attTable} '
        query2 += '(' + ','.join([f'[{c}]' for c in self.a_cols]) + ')'
        query2 += f' VALUES (' + ','.join(['?' for c in range(len(self.a_cols))]) + ')'
        values2 = []

        for i, current in enumerate(self.data_attribs, 1):
            vals = tuple([current[c] for c in self.a_cols])
            values2.append(vals)
            if i % 900 == 0:
                print(f"insertando atributo {i}")
                self.execute_query(query2, 'insert', values2)
                values2 = []
        if values2:
            self.execute_query(query2, 'insert', values2)

        #insert data for product table
        query3 = f'INSERT INTO {self.productTable} '
        query3 += '(' + ','.join([f'[{c}]' for c in self.p_cols]) + ')'
        query3 += f' VALUES (' + ','.join(['?' for c in range(len(self.p_cols))]) + ')'
        values3 = []

        for i, current in enumerate(self.data_products, 1):
            vals = tuple([current[c] for c in self.p_cols])
            values3.append(vals)
            if i % 900 == 0:
                print(f"insertando producto {i}")
                self.execute_query(query3, 'insert', values3)
                values3 = []
        if values3:
            self.execute_query(query3, 'insert', values3)

    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        # print("Limpiando variante")
        # self.cleanData()
        print("Obteniendo variante")
        self.getData()
        print("Generando Query")
        self.insert_data()
        #query=self.getInsertQuery()
        #self.executeQuery(query)
