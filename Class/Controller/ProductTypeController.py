from typing import overload

import numpy as np

from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import format_record, get_col_dtype
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class ProductTypeController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.table2 = tablas['atributo']
        c_t = np.array([ct for ct in get_col_dtype(self.table2)])
        self.atrb_cols = c_t[:, 0].tolist()
        self.atrb_ctypes = c_t[:, 1].tolist()
        self.atrb_datas = []

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/product_types.json?limit=50&expand=[attributes]'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current['attributos'] = current['attributes']
                del current['attributes']

                current = format_record(current, self.cols, self.ctypes)

                if type(current['attributos']) is str:
                    current['attributos'] = current['attributos'].replace("'", '"')
                    current['attributos'] = current['attributos'].replace("None", "null")
                    current['attributos'] = json.loads(current['attributos'])
                    for att in current['attributos']['items']:
                        att['idTipoProducto'] = current['id']
                        att = format_record(att, self.atrb_cols, self.atrb_ctypes)
                        self.atrb_datas.append(att)

                current['attributos'] = current['attributos']['href']

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
        for current in self.datas:
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
        self.execute_query(query, 'insert', values)

        atrb_query = f'INSERT INTO {self.table2} '
        atrb_query += '(' + ','.join([f'[{c}]' for c in self.atrb_cols]) + ')'
        atrb_query += f' VALUES (' + ','.join(['?' for c in range(len(self.atrb_cols))]) + ')'
        atrb_values = []
        for att in self.atrb_datas:
            if "options" in att and isinstance(att["options"], str):
                att["options"] = att["options"].replace('|', '')
            else:
                att["options"] = ""

            atrb_vals = tuple([att[c] for c in self.atrb_cols])
            atrb_values.append(atrb_vals)
        self.execute_query(atrb_query, 'insert', atrb_values)

    def execute_logic(self):
        print(f"Limpiando {self.table}")
        self.clear_table()
        print(f"Limpiando {self.table2}")
        self.clear_table(self.table2)
        print(f"Obteniendo {self.table}")
        self.get_data()
        print("Generando Query")
        self.insert_data()
