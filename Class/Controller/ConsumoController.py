import numpy as np

from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import get_col_dtype, format_record
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class ConsumoController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.table2 = tablas["consumoDetalle"]
        c_t = np.array([ct for ct in get_col_dtype(self.table2)])
        self.table2_cols = c_t[:, 0].tolist()
        self.table2_ctypes = c_t[:, 1].tolist()
        self.table2_datas = []

    def get_data(self):
        params = "&expand=[details]"
        url = os.getenv('API_URL_BASE') + '/stocks/consumptions.json?limit=50&offset=0' + params
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current["imagestionCcDescription"] = current["imagestionCcdescription"]
                current['idOficina'] = current["office"]["id"]
                current['idUsuario'] = current["user"]["id"]
                for detail in current["details"]["items"]:
                    detail['idVariante'] = detail["variant"]["id"]
                    detail['idConsumo'] = current["id"]

                    detail = format_record(detail, self.table2_cols, self.table2_ctypes)
                    self.table2_datas.append(detail)

                current['details'] = current["details"]["href"]
                current = format_record(current, self.cols, self.ctypes)
                self.datas.append(current)

            if "next" in response:
                url = response["next"] + params
            else:
                break

    def insert_data(self):
        query = f'INSERT INTO {self.table} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 50 == 0:
                print(f"insertando consumo {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)

        query = f'INSERT INTO {self.table2} '
        query += '(' + ','.join([f'[{c}]' for c in self.table2_cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.table2_cols))]) + ')'
        values = []
        for i, current in enumerate(self.table2_datas, 1):
            vals = tuple([current[c] for c in self.table2_cols])
            values.append(vals)
            if i % 50 == 0:
                print(f"insertando detalle consumo {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)

    def execute_logic(self):
        print(f"Limpiando {self.table}")
        self.clear_table()
        print(f"Limpiando {self.table2}")
        self.clear_table(self.table2)
        print("Obteniendo datos")
        self.get_data()
        print("Generando Query")
        self.insert_data()
