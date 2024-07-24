from Class.Controller.DocumentoController import DocumentoController

from datetime import datetime,timedelta
import sys

if(len(sys.argv)>2):
    firstDay=datetime.strptime(sys.argv[1],"%Y-%m-%d")
    lastDay=firstDay+timedelta(days=int(sys.argv[2]))
    #lastDay=datetime.now().strftime("%Y-%m-%d")
    #lastDay=datetime.strptime(lastDay,"%Y-%m-%d")
    #firstDay=firstDay-timedelta(days=int(sys.argv[2]))
    print(firstDay,lastDay)
 #   doc=DocumentController(datetime.timestamp(firstDay),datetime.timestamp(lastDay))
    print(datetime.timestamp(firstDay),',',datetime.timestamp(lastDay))
#    doc.process()
#    doc=DocumentoController(datetime.timestamp(firstDay),datetime.timestamp(lastDay))
#    doc.executelogic()
else:
    lastDay=datetime.now().strftime("%Y-%m-%d")
    lastDay=datetime.strptime(lastDay,"%Y-%m-%d")
    firstDay=lastDay-timedelta(days=30)
    print(firstDay,lastDay)
 #   doc=DocumentController(datetime.timestamp(firstDay),datetime.timestamp(lastDay))
    print(datetime.timestamp(firstDay),',',datetime.timestamp(lastDay))
#    doc.process()
#    doc=DocumentoController(datetime.timestamp(firstDay),datetime.timestamp(lastDay))
#    doc.executelogic()