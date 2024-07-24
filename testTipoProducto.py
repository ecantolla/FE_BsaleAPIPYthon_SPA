import requests
import json
from Class.Models.TipoProducto import TipoProducto
acumulado=0
url = 'https://api.bsale.cl/v1/product_types.json'
headers = {'Accept': 'application/json','access_token':'6de4c01b2a3d7f64153f0e4f96b1c1f51218be56'}
req = requests.get(url+"?offset="+str(acumulado), headers=headers)
response=json.loads(req.text)
flag=True
tpList="("
while(flag):
    if("next" in response):
        flag=True
    else:
        flag=False
    print(flag)
    for current in response["items"]:
        attHref=current["attributes"]["href"]
        if("attributes" not in current):
            attHref='null'
        tp=TipoProducto(current["id"],current["name"],current["isEditable"],current["state"],current["imagestionCategoryId"],current["prestashopCategoryId"],attHref)
        tp.createOrUpdate()