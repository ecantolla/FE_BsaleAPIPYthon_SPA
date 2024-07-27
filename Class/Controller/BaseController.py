from Class.Models.tablas import tablas
from Class.Models.ListaPrecio import ListaPrecio
from Class.ConnectionHandler import ConnectionHandler
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class BaseController:
    def __init__(self) -> None:
        self.con=ConnectionHandler()
        pass
    def listaPrecio(self):
        self.con.connect()
        self.con.executeQuery("delete from "+tablas["listaPrecio"])
        self.con.commitChange()
        url = os.getenv('API_URL_BASE') + '/price_lists.json?limit=50'
        flag=True
        headers = {'Accept': 'application/json','access_token': os.getenv('API_KEY')}
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
                    lp=ListaPrecio(item["id"],item["name"],item["description"],item["state"],item["details"]["href"])
                    lp.save()
    def detalleListaPrecio(self):
        
        pass
