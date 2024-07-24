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
            self.conn=pyodbc.connect('Driver={SQL Server};SERVER='+self.host+';DATABASE='+self.database+';UID='+self.user+';PWD='+self.passwd)
            return self.conn
        except:
            print("no hay conexion")
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
