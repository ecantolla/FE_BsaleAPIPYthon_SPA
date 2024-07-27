from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TipoDocumentoController:
    def __init__(self):
        self.table=tablas["tipoDocumento"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/document_types.json?limit=50'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            if("next" in response):
                flag=True
                url=response["next"]+''
            else:
                flag=False
            for current in response["items"]:
                self.datas.append(current)
    def getInsertQuery(self):
        query=f"""INSERT INTO {self.table}
            ([id]
            ,[name]
            ,[initialNumber]
            ,[codeSii]
            ,[isElectronicDocument]
            ,[breakdownTax]
            ,[use]
            ,[isSalesNote]
            ,[isExempt]
            ,[restrictsTax]
            ,[useClient]
            ,[thermalPrinter]
            ,[state]
            ,[copyNumber]
            ,[isCreditNote]
            ,[continuedHigh]
            ,[ledgerAccount]
            ,[ipadPrint]
            ,[ipadPrintHigh]
            ,[restrictClientType]
            ,[idTipoLibro])
            VALUES"""
        for current in self.datas:
            idBookType='null'
            if('book_type' in current):
                idBookType=current["book_type"]["id"]
            query=query+f"""
                ({current["id"]}
                ,'{current["name"]}'
                ,{current["initialNumber"]}
                ,'{current["codeSii"]}'
                ,{current["isElectronicDocument"]}
                ,{current["breakdownTax"]}
                ,{current["use"]}
                ,{current["isSalesNote"]}
                ,{current["isExempt"]}
                ,{current["restrictsTax"]}
                ,{current["useClient"]}
                ,{current["thermalPrinter"]}
                ,{current["state"]}
                ,{current["copyNumber"]}
                ,{current["isCreditNote"]}
                ,{current["continuedHigh"]}
                ,'{current["ledgerAccount"]}'
                ,{current["ipadPrint"]}
                ,{current["ipadPrintHigh"]}
                ,{current["restrictClientType"]}
                ,{idBookType}),"""
        
        query=query.replace("'None'",'null')
        query=query[:-1]
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando tipo documento")
        self.executeQuery(self.cleanData())
        print("Obteniendo tipo documento")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)
