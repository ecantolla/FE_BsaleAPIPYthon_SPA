from Class.Models.tablas import tablas, old_tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class ClienteController:
    def __init__(self):
        self.table=tablas["cliente"]
        self.oldtable= old_tablas["cliente"]
        self.datas=[]

    def cleanData(self):
        query=f"""delete from {self.table}"""
        self.executeQuery(query)
        return query
    def searchRow(self,data):
        for key in data:
            if key in ("createdAt", "updatedAt"):
                if data[key] in (None, ''):
                    data[key]=0
            if data[key] is None:
                data[key]=''
            elif type(data[key])==dict:
                data[key]=data[key]['href']
            
        query=f"""SELECT * FROM {self.table}
        WHERE id={data["id"]}
        AND firstName='{data["firstName"]}'
        AND lastName='{data["lastName"]}'
        AND email='{data["email"]}'
        AND code='{data["code"]}'
        AND phone='{data["phone"]}'
        AND company='{data["company"]}'
        AND note='{data["note"]}'
        AND facebook='{data["facebook"]}'
        AND twitter='{data["twitter"]}'
        AND hasCredit={data["hasCredit"]}
        AND maxCredit={data["maxCredit"]}
        AND state={data["state"]}
        AND activity='{data["activity"]}'
        AND city='{data["city"]}'
        AND municipality='{data["municipality"]}'
        AND address='{data["addresses"]}'
        AND companyOrPerson={data["companyOrPerson"]}
        AND accumulatePoints={data["accumulatePoints"]}
        AND points={data["points"]}
        AND pointsUpdated='{data["pointsUpdated"]}'
        AND sendDte={data["sendDte"]}
        AND isForeigner={data["isForeigner"]}
        AND prestashopClientId={data["prestashopClienId"]}
        AND createdAt=NULL
        AND updatedAt=NULL"""
        
        conn=ConnectionHandler()
        conn.connect()
        result = conn.executeQuery(query)
        breakpoint()
        #result = conn.getCursor().fetchone()
        conn.closeConnection()
        return result is not None
        #return result
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/clients.json?limit=50'
        flag=True
        headers = {'Accept': 'application/json','access_token': os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            if("next" in response):
                flag=True
                url=response["next"]+''
            else:
                flag=False
            for current in response["items"]:
                if not self.searchRow(current):
                    self.datas.append(current)
                else:
                    print(f"El cliente {current['id']} ya existe")
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
            if "prestashopClienId" in current:
                presta={current["prestashopClienId"]}

            query=query+f"""
                ({current["id"]}
                ,'{current["firstName"]}'
                ,'{current["lastName"]}'
                ,'{current["email"]}'
                ,'{current["code"]}'
                ,'{current["phone"]}'
                ,'{current["company"]}'
                ,'{current["note"]}'
                ,{current["facebook"] if current["facebook"] is not None else 'null'}
                ,{current["twitter"] if current["twitter"] is not None else 'null'}
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
                ,{current["pointsUpdated"]}
                ,{current["sendDte"]}
                ,{current["isForeigner"]}
                ,{presta}
                ,{current["createdAt"] if current["createdAt"] is not None else ""}
                ,{current["updatedAt"] if current["updatedAt"] is not None else ""}),"""
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
        """ print("Limpiando clientes")
        self.executeQuery(self.cleanData()) """
        print("Obteniendo clientes")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        self.executeQuery(query)
