import os

from dotenv import load_dotenv

from Class.ConnectionHandler import ConnectionHandler
from Class.Controller.Herlpers import get_col_dtype
from Class.Models.tablas import tablas
import numpy as np
load_dotenv(override=True)


class AbstractController:

    def __init__(self, tabla):
        self.table = tablas[tabla]
        self.datas = []
        c_t = np.array([ct for ct in get_col_dtype(self.table)])
        self.cols = c_t[:, 0].tolist()
        self.ctypes = c_t[:, 1].tolist()

    def clear_table(self, table=None):
        table = table if table else self.table
        query = f"TRUNCATE TABLE {table}"
        self.execute_query(query, 'truncate')

    def row_exists(self, data, table=None):
        table = table if table else self.table
        query = f"SELECT * FROM {table} WHERE "
        filtered_data = {k: v for k, v in data.items() if k in self.cols and v is not None}
        cols = list(filtered_data.keys())
        vals = tuple(filtered_data.values())
        query += " AND ".join([f"{c} = ?" for c in cols]) + ";"
        result = self.execute_query(query, 'select', vals)
        return True if result else False

    def get_data(self):
        pass

    def insert_data(self):
        pass

    def execute_query(self, query, query_type, values=None):
        conn = ConnectionHandler()
        conn.connect()
        result = conn.executeQuery(query, query_type, values)
        conn.closeConnection()
        return result

    def execute_logic(self):
        pass
