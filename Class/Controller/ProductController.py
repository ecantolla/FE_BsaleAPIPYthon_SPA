from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import format_record
from Class.Models.tablas import tablas
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class ProductController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/products.json?limit=50&expand=[product_type]'
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current['idTipoProducto'] = current["product_type"]["id"]
                pt = current["product_type"]
                current = format_record(current, self.cols, self.ctypes)
                current["product_type"] = pt
                self.datas.append(current)

            if "next" in response['items']:
                url = response["next"]
            else:
                break

    def insert_data(self):
        query = f'INSERT INTO {self.table} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []

        product_types = {}  # Store unique product type data

        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)

            type_data = current["product_type"]
            product_type_id = current['idTipoProducto']
            if product_type_id not in product_types:
                # If product type is not in the dictionary, add it
                product_types[product_type_id] = type_data

            if i % 900 == 0:
                print("inserting 900 products")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)
        return product_types

    def execute_logic(self):
        print("Limpiando products")
        self.clear_table()
        print("Obteniendo products")
        self.get_data()
        print("Generando Query")
        product_types = self.insert_data()
        print("Termino query de producto")

        print("Iniciando query de tipo de producto")
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

            self.execute_query(single_type_query, 'merge')
        print("Termino query de tipo de producto en base a productos")
