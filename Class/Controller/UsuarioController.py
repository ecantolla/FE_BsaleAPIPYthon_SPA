from Class.Controller.Herlpers import *
import requests
import json
import os
from Class.Controller.AbstractController import AbstractController
from dotenv import load_dotenv

load_dotenv(override=True)


class UsuarioController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/users.json?limit=50'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                if 'office' in current:
                    current['idSucursal'] = current['office']['id']
                    del current['office']
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
            print('no se insertaron datos de usuario.')
            print(e)

    def execute_logic(self):
        print("Limpiando Usuario")
        self.clear_table()
        print("Obteniendo usuarios")
        self.get_data()
        print("Generando Query")
        self.insert_data()
