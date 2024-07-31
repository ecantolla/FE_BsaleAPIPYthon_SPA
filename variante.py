from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime,timedelta
from Class.ConnectionHandler import ConnectionHandler

con=ConnectionHandler()
url = os.getenv('API_URL_BASE') + '/variants.json'
headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
cant=25
acumulado=0
con.connect()
while(cant>=25):
    currentTime=datetime.now()
    print(url+"?offset="+str(acumulado))
    req = requests.get(url+"?offset="+str(acumulado), headers=headers)
    response=json.loads(req.text)
    
    cant=0
    for current in response["items"]:
        cant=cant+1
        id=current["id"]
        link=current["costs"]
        result=requests.get(link["href"],headers=headers)
        cost=json.loads(result.text)["averageCost"]
        query="update variante set costoPromedio="+str(cost)+" where id="+str(id)
        con.executeQuery(query)
        con.commitChange()
        print(query)
    print(cant)
    acumulado=acumulado+cant
    print(datetime.now()-currentTime)