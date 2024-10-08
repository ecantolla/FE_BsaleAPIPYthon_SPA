import numpy as np

from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import format_record, get_col_dtype
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class ListaPrecioController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.table2 = tablas["detalleListaPrecio"]
        c_t = np.array([ct for ct in get_col_dtype(self.table2)])
        self.dlp_cols = c_t[:, 0].tolist()
        self.dlp_ctypes = c_t[:, 1].tolist()
        self.dlp_datas = []

    def get_data(self):
        params = "&expand=[coin,details]"
        url = os.getenv('API_URL_BASE') + '/price_lists.json?limit=50' + params
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                for detail in current["details"]["items"]:
                    detail["idVariante"] = detail["variant"]["id"]
                    del detail["variant"]["id"]
                    detail["idListaPrecio"] = current["id"]
                    detail = format_record(detail, self.dlp_cols, self.dlp_ctypes)
                    self.dlp_datas.append(detail)

                current["details"] = current["details"]["href"]
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
        for current in self.datas:
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
        self.execute_query(query, 'insert', values)


        query = f'INSERT INTO {self.table2} '
        query += '(' + ','.join([f'[{c}]' for c in self.dlp_cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.dlp_cols))]) + ')'
        values = []
        for details in self.dlp_datas:
            vals = tuple([details[c] for c in self.dlp_cols])
            values.append(vals)
        self.execute_query(query, 'insert', values)

    def del74(self):
        query = """
        DELETE FROM DETALLE_LISTA_PRECIO
        WHERE idListaPrecio = 7
        AND idVariante IN (
            SELECT idVariante
            FROM DETALLE_LISTA_PRECIO
            WHERE idListaPrecio IN (7, 4)
            GROUP BY idVariante
            HAVING COUNT(*) > 1
        );
        """
        self.execute_query(query, 'delete')

    def execute_logic(self):
        print(f"Limpiando {self.table}")
        self.clear_table()
        print(f"Limpiando {self.table2}")
        self.clear_table(self.table2)
        print("Obteniendo descuento")
        self.get_data()
        print("Generando Query")
        self.insert_data()
        self.del74()
