from Class.Controller.DocumentoController import DocumentoController

from datetime import datetime,timedelta
import sys

lastDay=datetime.now().strftime("%Y-%m-%d")
lastDay=datetime.strptime(lastDay,"%Y-%m-%d")
firstDay=lastDay-timedelta(days=30)
print(firstDay,lastDay)
doc=DocumentoController(datetime.timestamp(firstDay),datetime.timestamp(lastDay))
print(datetime.timestamp(firstDay),',',datetime.timestamp(lastDay))
doc.getDocument()