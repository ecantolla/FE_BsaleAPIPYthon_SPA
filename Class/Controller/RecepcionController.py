from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RecepcionController:
    def __init__(self):
        self.table=tablas["recepcion"]
        self.details=tablas["recepcionDetalle"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        self.executeQuery("delete from "+self.details)
        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/stocks/receptions.json?limit=50&offset=0&expand=[details]'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            print(url)
            if("next" in response):
                flag=True
                url=response["next"]+'&expand=[details]'
            else:
                flag=False
            for current in response["items"]:
                self.datas.append(current)
    def getInsertQuery(self):
        query=f"""INSERT INTO {self.table}
                ([id]
                ,[admissionDate]
                ,[document]
                ,[documentNumber]
                ,[note]
                ,[imagestionCctId]
                ,[imagestionCcDescription]
                ,[internalDispatchId]
                ,[idOficina]
                ,[idUsuario]
                ,[details])
            VALUES"""
        i=0
        contDetail=0
        detailQuery=f"""
            INSERT INTO {self.details}
                ([id]
                ,[quantity]
                ,[cost]
                ,[variantStock]
                ,[serialNumber]
                ,[idVariante]
                ,[idRecepcion])
            VALUES
        """
        for current in self.datas:
            i=i+1
            query=query+f"""
                ({current["id"]}
                ,{current["admissionDate"]}
                ,'{current["document"]}'
                ,'{current["documentNumber"]}'
                ,'{current["note"]}'
                ,{current["imagestionCctId"]}
                ,'{current["imagestionCcDescription"]}'
                ,{current["internalDispatchId"]}
                ,{current["office"]["id"]}
                ,{current["user"]["id"]}
                ,'{current["details"]["href"]}'),"""
            
            for detail in current["details"]["items"]:
                contDetail=contDetail+1
                detailQuery=detailQuery+f"""
                    ({detail["id"]}
                    ,{detail["quantity"]}
                    ,{detail["cost"]}
                    ,{detail["variantStock"]}
                    ,'{detail["serialNumber"]}'
                    ,{detail["variant"]["id"]}
                    ,{current["id"]}),"""
                if contDetail>900:
                    print("ingresando 900 detalles")
                    contDetail=0
                    detailQuery=detailQuery[:-1]
                    self.executeQuery(detailQuery)
                    detailQuery=f"""
                        INSERT INTO {self.details}
                            ([id]
                            ,[quantity]
                            ,[cost]
                            ,[variantStock]
                            ,[serialNumber]
                            ,[idVariante]
                            ,[idRecepcion])
                        VALUES
                    """

            if i>900:
                i=0
                query=query[:-1]
                print("ingresando 900 recepcion")
                self.executeQuery(query)
                query=f"""INSERT INTO {self.table}
                    ([id]
                    ,[admissionDate]
                    ,[document]
                    ,[documentNumber]
                    ,[note]
                    ,[imagestionCctId]
                    ,[imagestionCcDescription]
                    ,[internalDispatchId]
                    ,[idOficina]
                    ,[idUsuario]
                    ,[details])
                VALUES"""
        detailQuery=detailQuery[:-1]
        self.executeQuery(detailQuery)
        query=query.replace("'None'",'null')
        query=query[:-1]
        self.executeQuery(query)
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando Recepcion")
        self.executeQuery(self.cleanData())
        print("Obteniendo recepcion")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        #self.executeQuery(query)
