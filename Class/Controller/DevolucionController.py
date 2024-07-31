from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import *
import requests
import json
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv(override=True)


class DevolucionController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.details = tablas["detalle_devolucion"]
        d_t = np.array([dt for dt in get_col_dtype(self.details)])
        self.d_cols = d_t[:, 0].tolist()
        self.dc_types = d_t[:, 1].tolist()
        self.detail_values = []

    def get_data(self):
        url = os.getenv('API_URL_BASE') + '/returns.json?limit=50&expand=[details]'
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            
            for current in response["items"]:
                items_details = None
                if 'details' in current:
                    items_details = current['details']['items']
                    current['details'] = current['details']['href']
                else:
                    current['details'] = None

                current['idOficina'] = current['office']['id'] if 'office' in current else None
                current['idUsuario'] = current['user']['id'] if 'user' in current else None
                current['idDocumentoReferencia'] = current['reference_document']['id'] if 'reference_document' in current else None
                current['idDocumentoCredito'] = current['credit_note']['id'] if 'credit_note' in current else None
                
                current_dev = format_record(current, self.cols, self.ctypes)
                if not self.row_exists(current_dev):
                    self.datas.append(current_dev)
            
                for detail in items_details:
                    detail['idDevolucion'] = current['id']
                    if 'documentDetailId' in detail:
                        detail['idDetalleDocumento'] = detail['documentDetailId']
                        del detail['documentDetailId']
                    else:
                        detail['idDetalleDocumento'] = None
                    current_detail = format_record(detail, self.d_cols, self.dc_types)
                    if not self.row_exists(current_detail, self.details):
                        self.detail_values.append(current_detail)
            
            if "next" in response:
                url = response["next"]+'&expand=[details]'
            else:
                break

    def insert_data(self):
        #insert data for devolucion table
        query = f'INSERT INTO {self.table} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += f' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 900 == 0:
                print(f"insertando devolucion {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            self.execute_query(query, 'insert', values)

        #insert data for detalle devolucion table
        query2 = f'INSERT INTO {self.details} '
        query2 += '(' + ','.join([f'[{c}]' for c in self.d_cols]) + ')'
        query2 += f' VALUES (' + ','.join(['?' for c in range(len(self.d_cols))]) + ')'
        values2 = []
        for i, current in enumerate(self.detail_values, 1):
            vals = tuple([current[c] for c in self.d_cols])
            values2.append(vals)
            if i % 900 == 0:
                print(f"insertando detalle devolucion {i}")
                self.execute_query(query2, 'insert', values2)
                values2 = []
        if values2:
            self.execute_query(query2, 'insert', values2)

    def execute_logic(self):
        print("Limpiando devoluciones")
        self.clear_table("detalle_devolucion")
        self.clear_table()
        print("Obteniendo devoluciones")
        self.get_data()
        print("Generando Query")
        self.insert_data()
