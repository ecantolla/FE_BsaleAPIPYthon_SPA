from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import *
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class ClienteController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.endpoint = '/clients.json?limit=50'

    def get_data(self):
        url = os.getenv('API_URL_BASE') + self.endpoint
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current['prestashopClientId'] = current['prestashopClienId']
                del current['prestashopClienId']

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
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 900 == 0:
                print(f"insertando cliente {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)

    def execute_logic(self):
        print(f"Limpiando {self.table}")
        self.clear_table()
        print(f"Obteniendo {self.table}")
        self.get_data()
        print("Generando Query")
        self.insert_data()
