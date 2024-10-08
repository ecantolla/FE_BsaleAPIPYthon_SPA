import requests
import json
from Class.Models.TipoDocumento import TipoDocumento
acumulado=0
url = os.getenv('API_URL_BASE') + '/document_types.json'
headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
req = requests.get(url+"?offset="+str(acumulado), headers=headers)
response=json.loads(req.text)
flag=True
tpList="("
while(flag):
    if("next" in response):
        flag=True
    else:
        flag=False
    for current in response["items"]:
        if("book_type" in current):
            tp=TipoDocumento(500,current["name"],current["initialNumber"],current["codeSii"],current["isElectronicDocument"],current["breakdownTax"],current["use"],current["isSalesNote"],current["isExempt"],current["restrictsTax"],current["useClient"],current["thermalPrinter"],current["state"],current["copyNumber"],current["isCreditNote"],current["continuedHigh"],current["ledgerAccount"],current["ipadPrint"],current["ipadPrintHigh"],current["restrictClientType"],current["book_type"]["id"])
        else:
            tp=TipoDocumento(500,current["name"],current["initialNumber"],current["codeSii"],current["isElectronicDocument"],current["breakdownTax"],current["use"],current["isSalesNote"],current["isExempt"],current["restrictsTax"],current["useClient"],current["thermalPrinter"],current["state"],current["copyNumber"],current["isCreditNote"],current["continuedHigh"],current["ledgerAccount"],current["ipadPrint"],current["ipadPrintHigh"],current["restrictClientType"],None)
        tpList=tpList+str(tp.updateOrCreate())+","
    tpList=tpList+"0)"
    tp.clean(tpList)