from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ClienteController:
    def __init__(self):
        self.table=tablas["cliente"]
        self.datas=[]

    def cleanData(self):
        query=f"""delete from {self.table}"""
        self.executeQuery(query)
        return query
    def getData(self):
        url = os.getenv('OLD_API_URL_BASE') + '/clients.json?limit=50'
        flag=True
        headers = {'Accept': 'application/json','access_token': os.getenv('OLD_API_KEY')}
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
        query=f"""INSERT INTO {tablas["cliente"]}
                ([id]
                ,[firstName]
                ,[lastName]
                ,[email]
                ,[code]
                ,[phone]
                ,[company]
                ,[note]
                ,[facebook]
                ,[twitter]
                ,[hasCredit]
                ,[maxCredit]
                ,[state]
                ,[activity]
                ,[city]
                ,[municipality]
                ,[address]
                ,[companyOrPerson]
                ,[accumulatePoints]
                ,[points]
                ,[pointsUpdated]
                ,[sendDte]
                ,[isForeigner]
                ,[prestashopClientId]
                ,[createdAt]
                ,[updatedAt])
            VALUES"""
        i=0
        for current in self.datas:
            i=i+1
            presta=0
            if "prestashopClientId" in current:
                presta={current["prestashopClientId"]}
            pointsUpdated="''"
            query=query+f"""
                ({current["id"]}
                ,'{current["firstName"]}'
                ,'{current["lastName"]}'
                ,'{current["email"]}'
                ,'{current["code"]}'
                ,'{current["phone"]}'
                ,'{current["company"]}'
                ,'{current["note"]}'
                ,null
                ,null
                ,{current["hasCredit"]}
                ,{current["maxCredit"]}
                ,{current["state"]}
                ,'{current["activity"]}'
                ,'{current["city"]}'
                ,'{current["municipality"]}'
                ,'{current["address"]}'
                ,{current["companyOrPerson"]}
                ,{current["accumulatePoints"]}
                ,{current["points"]}
                ,{pointsUpdated}
                ,{current["sendDte"]}
                ,{current["isForeigner"]}
                ,{presta}
                ,null
                ,null),"""
            if i>900:
                i=0
                print("insertando 900 clientes")
                query=query.replace("'None'",'null')
                query=query.replace('None','null')
                query=query[:-1]
                self.executeQuery(query)
                query=f"""INSERT INTO {tablas["cliente"]}
                        ([id]
                        ,[firstName]
                        ,[lastName]
                        ,[email]
                        ,[code]
                        ,[phone]
                        ,[company]
                        ,[note]
                        ,[facebook]
                        ,[twitter]
                        ,[hasCredit]
                        ,[maxCredit]
                        ,[state]
                        ,[activity]
                        ,[city]
                        ,[municipality]
                        ,[address]
                        ,[companyOrPerson]
                        ,[accumulatePoints]
                        ,[points]
                        ,[pointsUpdated]
                        ,[sendDte]
                        ,[isForeigner]
                        ,[prestashopClientId]
                        ,[createdAt]
                        ,[updatedAt])
                    VALUES"""
            
        query=query.replace("'None'",'null')
        query=query.replace('None','null')
        query=query[:-1]
        file=open("test.txt","w")
        file.write(query)
        file.close()
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando clientes")
        self.executeQuery(self.cleanData())
        print("Obteniendo clientes")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)