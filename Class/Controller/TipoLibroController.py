from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import format_record
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class TipoLibroController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/book_types.json'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                current = format_record(current, self.cols, self.ctypes)
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
        self.execute_query(query, 'insert', values)

    def execute_logic(self):
        print("Limpiando tipo libro")
        self.clear_table()
        print("Obteniendo tipo libro")
        self.get_data()
        print("Generando Query")
        self.insert_data()
