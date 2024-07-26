from Class.Models.Variante import Variante
from Class.Models.ValorAtributo import ValotAtributo
from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

from datetime import datetime
class VarianteController:
    def __init__(self):
        self.process="Iniciando"
        self.con=ConnectionHandler()
        self.con.connect()
        #self.con.executeQuery("delete from "+tablas["variante"])
        #self.con.commitChange()
        #self.con.closeConnection()
    def getInsertVariant(self):
        variantes=[]
        url = os.getenv('OLD_API_URL_BASE') + '/variants.json?limit=50&expand=[costs,product,attribute_values]'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('OLD_API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            if("next" in response):
                flag=True
                url=response["next"]+'&expand=[costs,product,attribute_values]'
            else:
                flag=False
            if(response["count"]>0):
                for item in response["items"]:
                    variantes.append(item)
            flag=False
        return variantes
        
    def findData(self):
        currentTime=datetime.now()
        url = os.getenv('OLD_API_URL_BASE') + '/variants.json?limit=50'
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('OLD_API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            if("next" in response):
                flag=True
                url=response["next"]
            else:
                flag=False
            if(response["count"]>0):
                for item in response["items"]:
                    #por cada variante buscar costo promedio
                    costoPromedio=0
                    if("costs" in item):
                        try:
                            result=requests.get(item["costs"]["href"],headers=headers)
                            costoPromedio=json.loads(result.text)["averageCost"]
                        except:
                            print("Error de acceso")

                    currentVariante=Variante(item["id"],item["description"],item["unlimitedStock"],item["allowNegativeStock"],item["state"],item["barCode"],item["code"],item["imagestionCenterCost"],item["imagestionAccount"],item["imagestionConceptCod"],item["imagestionProyectCod"],item["imagestionCategoryCod"],item["imagestionProductId"],item["serialNumber"],item["prestashopCombinationId"],item["prestashopValueId"],item["product"]["id"],item["attribute_values"]["href"],item["costs"]["href"],costoPromedio)
                    currentVariante.save()
            print(datetime.now()-currentTime)

    def getAtributos(self):
        self.con.connect()
        query="select id,atributos from "+tablas["variante"]
        result=self.con.executeQuery(query)
        for current in result:
            query="delete from "+tablas["valorAtributo"]+" where idVariante="+str(current[0])
            self.con.executeQuery(query)
            self.con.commitChange()
            
            flag=True
            url=current[1]+"?limit=50"
            headers = {'Accept': 'application/json','access_token':os.getenv('OLD_API_KEY')}
            while(flag):
                req = requests.get(url, headers=headers)
                response=json.loads(req.text)
                if("next" in response):
                    flag=True
                    url=response["next"]
                else:
                    flag=False
                if(response["count"]>0):
                    for item in response["items"]:
                        att='null'
                        if("attribute" in item):
                            att=item["attribute"]["id"]
                        vp=ValotAtributo(item["id"],item["description"],att,current[0])
                        vp.save()
