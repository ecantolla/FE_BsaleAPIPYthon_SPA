import requests
import json
from Class.Models.Producto import Producto

def processProduct():
    acumulado=0
    url = 'https://api.bsale.cl/v1/products.json?limit=50'
    flag=True
    while(flag):
        print(url)
        headers = {'Accept': 'application/json','access_token':'6de4c01b2a3d7f64153f0e4f96b1c1f51218be56'}
        req = requests.get(url+"?offset="+str(acumulado), headers=headers)
        response=json.loads(req.text)
        if("next" in response):
            flag=True
            url=response["next"]
        else:
            flag=False
        for current in response["items"]:
            productType='null'
            variant='null'
            if("product_type" in current):
                productType=current["product_type"]["id"]
            if("variants" in current):    
                variant=current["variants"]["href"]
            currentProduct=Producto(current["id"],current["name"],current["description"],current["classification"],current["ledgerAccount"],current["costCenter"],current["allowDecimal"],current["stockControl"],current["printDetailPack"],current["state"],current["prestashopProductId"],current["presashopAttributeId"],productType,variant)
            currentProduct.createOrUpdate()