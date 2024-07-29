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
    
    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/variants.json?expand=[attribute_values,product,costs]&limit=50&offset=0'
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}

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

                #aqui se inserta en el array de variante
                current_variant = format_record(current, self.cols, self.ctypes)
                if not self.row_exists(current):
                    self.datas.append(current_variant)

                # aqui insertamos en el array de atributos
                for att in current["attribute_values"]["items"]:
                    att['idVariante'] = current['id']
                    att['idAtributo'] = att['attribute']['id']
                    att['description'] = att['description'].replace("'","''")
                    current_attrib = format_record(att, self.a_cols, self.ac_types)
                    if not self.row_exists(current_attrib, self.attTable):
                        self.data_attribs.append(current_attrib)                

                # aqui insertamos en el array de productos
                if 'product_type' in current['product']:
                    current['product']['idTipoProducto'] = current['product']['product_type']['id']
                current_product = format_record(current['product'], self.p_cols, self.pc_types)
                if not self.row_exists(current_product, self.productTable):
                    self.data_products.append(current_product)
                
            if "next" in response['items']:
                url = response["next"] + '&expand=[attribute_values,product,costs]'
            else:
                break

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

    def executelogic(self):        
        # print("Limpiando variante")
        # tablas = [self.table, self.attTable, self.productTable]
        # for tabla in tablas:
        #     self.clear_table(tabla)
        print("Obteniendo variante")
        self.get_data()
        print("Generando Query")
        self.insert_data()
