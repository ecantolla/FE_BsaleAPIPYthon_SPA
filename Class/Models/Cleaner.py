from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas
class Cleaner:
    def __init__(self):
        self.con=ConnectionHandler()
    def clean(self,table,condition):
        query="delete from "+table+" "+condition
        self.con.connect()
        self.con.executeQuery(query)
        self.con.commitChange()
        self.con.closeConnection()