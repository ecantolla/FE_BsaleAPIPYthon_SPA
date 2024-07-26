import pyodbc
import configparser
class ConnectionHandler:
    def __init__(self):
        config=configparser.ConfigParser()
        config.read('./config/config.ini')
        self.host=config["config"]["host"]
        self.database=config["config"]["database"]
        self.user=config["config"]["user"]
        self.passwd=config["config"]["passwd"]
        self.conn=None
    def connect(self):
        try:
            connectionString = f'Driver={{ODBC Driver 18 for SQL Server}};' \
                f'SERVER={self.host};' \
                f'DATABASE={self.database};' \
                f'UID={self.user};' \
                f'PWD={self.passwd};' \
                'Encrypt=no;TrustServerCertificate=yes'
            self.conn = pyodbc.connect(connectionString)
            return self.conn
        except Exception as e:
            print("no hay conexion: ", str(e))
            return None
    def executeQuery(self,query):
        self.connect()
        cursor=self.conn.cursor()
        result=cursor.execute(query)
        return result
    def closeConnection(self):
        self.conn.close()
    def commitChange(self):
        self.conn.commit()
