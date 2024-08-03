import pyodbc
import os


class ConnectionHandler:
    def __init__(self):
        self.host = os.getenv('HOST')
        self.database = os.getenv('DATABASE')
        self.user = os.getenv('USER')
        self.passwd = os.getenv('PASSWORD')
        self.conn = None

    def connect(self):
        try:
            connection_string = f'Driver={{SQL Server}};' \
                f'SERVER={self.host};' \
                f'DATABASE={self.database};' \
                f'UID={self.user};' \
                f'PWD={self.passwd};' \
                'Encrypt=no;TrustServerCertificate=yes'
            self.conn = pyodbc.connect(connection_string)
            return True
        except Exception as e:
            print("no hay conexion: ", str(e))
            return False

    def executeQuery(self, query, query_type, values=None):
        self.connect()
        cursor = self.conn.cursor()
        if values:
            if query_type == 'select':
                result = cursor.execute(query, values)
            else:
                # cursor.fast_executemany = True
                result = cursor.executemany(query, values)
        else:
            result = cursor.execute(query)

        if query_type in ('insert', 'truncate', 'delete'):
            cursor.commit()
        elif query_type == 'select':
            result = cursor.fetchall() if result else None
        cursor.close()
        return result

    def closeConnection(self):
        self.conn.close()
