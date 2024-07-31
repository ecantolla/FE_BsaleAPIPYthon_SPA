from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import format_record
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


class StockController(AbstractController):

    def __init__(self, tabla):
        super().__init__(tabla)

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/stocks.json?limit=50&offset=0'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current['idVariante'] = current["variant"]["id"]
                del current["variant"]["id"]
                current['idSucursal'] = current["office"]["id"]
                del current["office"]["id"]
                current = format_record(current, self.cols, self.ctypes)
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
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 900 == 0:
                print(f"insertando stocks {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)

    def execute_logic(self):
        print("Limpiando stock")
        self.clear_table()
        print("Obteniendo stock")
        self.get_data()
        print("Generando Query")
        self.insert_data()
