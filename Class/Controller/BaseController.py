from Class.Models.tablas import tablas
from Class.Models.ListaPrecio import ListaPrecio
from Class.ConnectionHandler import ConnectionHandler
import requests
import json

class BaseController:
    def __init__(self) -> None:
        self.con=ConnectionHandler()
        pass
    def listaPrecio(self):
        self.con.connect()
        self.con.executeQuery("delete from "+tablas["listaPrecio"])
        self.con.commitChange()
        url = 'https://api.bsale.cl/v1/price_lists.json?limit=50'
        flag=True
        headers = {'Accept': 'application/json','access_token':'6de4c01b2a3d7f64153f0e4f96b1c1f51218be56'}
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