from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import *
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class SucursalController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/offices.json'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:                
                current = format_record(current, self.cols, self.ctypes)
                if not self.row_exists(current):
                    self.datas.append(current)
                
            if "next" in response:
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
        try:
            self.execute_query(query, 'insert', values)
        except Exception as e:
            print('no se insertaron datos.')
            print(e)

    def execute_logic(self):
        print("Limpiando sucursales")
        self.clear_table()
        print("Obteniendo sucursales")
        self.get_data()
        print("Generando Query")
        self.insert_data()
