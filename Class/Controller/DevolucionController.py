from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DevolucionController:
    def __init__(self):
        self.table=tablas["devolucion"]
        self.details=tablas["detalle_devolucion"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        self.executeQuery("delete from "+self.details)

        return query
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/returns.json?limit=50&expand=[details]'
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
                ,[code]
                ,[returnDate]
                ,[motive]
                ,[type]
                ,[priceAdjustment]
                ,[editTexts]
                ,[amount]
                ,[idOficina]
                ,[idUsuario]
                ,[idDocumentoReferencia]
                ,[idDocumentoCredito]
                ,[details])
            VALUES"""
        i=0
        contDetail=0
        detailQuery=f"""
            INSERT INTO {self.details}
                ([id]
                ,[quantity]
                ,[quantityDevStock]
                ,[variantStock]
                ,[variantCost]
                ,[idDetalleDocumento]
                ,[idDevolucion])
            VALUES
            """
        for current in self.datas:
            
            i=i+1
            note=0
            if "credit_note" in current:
                note=current["credit_note"]["id"]
                if(note==946):
                    print("aca")
                print(note)
            else:
                print(current["id"])
            query=query+f"""
                ({current["id"]}
                ,'{current["code"]}'
                ,{current["returnDate"]}
                ,'{current["motive"]}'
                ,{current["type"]}
                ,{current["priceAdjustment"]}
                ,{current["editTexts"]}
                ,{current["amount"]}
                ,{current["office"]["id"]}
                ,{current["user"]["id"]}
                ,{current["reference_document"]["id"]}
                ,{note}
                ,'{current["details"]["href"]}'),"""
            
            for detail in current["details"]["items"]:
                contDetail=contDetail+1
                detailQuery=detailQuery+f"""
                    ({detail["id"]}
                    ,{detail["quantity"]}
                    ,{detail["quantityDevStock"]}
                    ,{detail["variantStock"]}
                    ,{detail["variantCost"]}
                    ,{detail["documentDetailId"]}
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
                            ,[quantityDevStock]
                            ,[variantStock]
                            ,[variantCost]
                            ,[idDetalleDocumento]
                            ,[idDevolucion])
                        VALUES            
                    """
            if i>900:
                i=0
                query=query[:-1]
                print("ingresando 900 devoluciones")
                self.executeQuery(query)
                query=f"""INSERT INTO {self.table}
                        ([id]
                        ,[code]
                        ,[returnDate]
                        ,[motive]
                        ,[type]
                        ,[priceAdjustment]
                        ,[editTexts]
                        ,[amount]
                        ,[idOficina]
                        ,[idUsuario]
                        ,[idDocumentoReferencia]
                        ,[idDocumentoCredito]
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
        print("Limpiando devoluciones")
        self.executeQuery(self.cleanData())
        print("Obteniendo devoluciones")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        #self.executeQuery(query)
