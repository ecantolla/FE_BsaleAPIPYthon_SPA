from Class.Models.tablas import tablas, old_tablas
from Class.ConnectionHandler import ConnectionHandler
from Class.Controller.Herlpers import *
import requests
import json
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()


class ClienteController:
    def __init__(self):
        self.table = tablas["cliente"]
        self.oldtable = old_tablas["cliente"]
        self.datas = []
        c_t = np.array([ct for ct in get_col_dtype(self.table)])
        self.cols = c_t[:, 0].tolist()
        self.ctypes = c_t[:, 1].tolist()

    def clear_table(self):
        query = f"TRUNCATE TABLE {self.table}"
        self.execute_query(query, 'truncate')

    def row_exists(self, data):
        query = f"SELECT * FROM {self.table} WHERE "
        filtered_data = {k: v for k, v in data.items() if k in self.cols and v is not None}
        cols = list(filtered_data.keys())
        vals = tuple(filtered_data.values())
        query += " AND ".join([f"{c} = ?" for c in cols]) + ";"
        result = self.execute_query(query, 'select', vals)
        return True if result else False

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/clients.json?limit=50'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        i = 0
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current['prestashopClientId'] = current['prestashopClienId']
                del current['prestashopClienId']

                current = format_record(current, self.cols, self.ctypes)

                if self.row_exists(current):
                    print(f"El cliente {current['id']} ya existe")
                    continue

                self.datas.append(current)
            if "next" in response:
                url = response["next"]
            else:
                break

    def insert_data(self):
        query = f'INSERT INTO {tablas["cliente"]} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 50 == 0:
                print(f"insertando cliente {i}")
                self.execute_query(query, 'insert', values)
                values = []

    def execute_query(self, query, query_type, values=None):
        conn = ConnectionHandler()
        conn.connect()
        result = conn.executeQuery(query, query_type, values)
        conn.closeConnection()
        return result

    def executelogic(self):
        # print("Limpiando clientes")
        # self.clear_table()
        print("Obteniendo clientes")
        self.get_data()
        print("Generando Query")
        self.insert_data()
