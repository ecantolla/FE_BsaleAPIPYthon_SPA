from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
from Class.Controller.Herlpers import *
import requests
import json
import os
from Class.Controller.AbstractController import AbstractController
from dotenv import load_dotenv

load_dotenv()


class UsuarioController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.offset = 0
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/users.json?limit=50&offset='+str(self.offset)
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                if 'office' in current:
                    current['idSucursal'] = current['office']['id']
                    del current['office']
                # print(current)
                # breakpoint()
                current = format_record(current, self.cols, self.ctypes)

                if self.row_exists(current):
                    print(f"El usuario {current['id']} ya existe")
                    continue

                self.datas.append(current)
            if "next" in response:
                url = response["next"]
            else:
                break

    def getInsertQuery(self):
        query = f'INSERT INTO {self.table} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
        try:
            self.execute_query(query, 'insert', values)
        except Exception as e:
            print('no se insertaron datos de usuario.')
            print(e)

        values = []

    def executelogic(self):
        # print("Limpiando Usuario")
        # self.executeQuery(self.cleanData())
        print("Obteniendo usuarios")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
