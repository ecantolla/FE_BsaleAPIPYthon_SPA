from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class DocumentoController:
    def __init__(self,inicio,fin):
        self.table=tablas["documento"]
        self.vendedor=tablas["vendedor"]
        self.detail=tablas["detalleDocumento"]
        self.inicio=inicio
        self.fin=fin
        self.datas=[]
    def cleanData(self):
        pass
    def getData(self):
        url = os.getenv('API_URL_BASE') + '/documents.json?limit=50&offset=0&emissiondaterange=['+str(self.inicio)+' ,'+str(self.fin)+']&expand=[details,sellers]'
        #1676430000.0 , 1678158000.0
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            print(url)
            if("next" in response):
                flag=True
                url=response["next"]+'&emissiondaterange=['+str(self.inicio)+' ,'+str(self.fin)+']&expand=[details,sellers]'
            else:
                flag=False
            if "items in response":
                for current in response["items"]:
                    self.datas.append(current)
    def setVendedorDefault(self):
        return f"""
            INSERT INTO {tablas["vendedor"]}
                ([idUsuario]
                ,[firstName]
                ,[lastName]
                ,[idDocumento])
            VALUES
        """
    def setDocumentDefault(self):
        return f"""
            INSERT INTO {self.table}
            ([id]
            ,[emissionDate]
            ,[expirationDate]
            ,[generationDate]
            ,[number]
            ,[serialNumber]
            ,[totalAmount]
            ,[netAmount]
            ,[taxAmount]
            ,[exemptAmount]
            ,[notExemptAmount]
            ,[exportTotalAmount]
            ,[exportNetAmount]
            ,[exportTaxAmount]
            ,[exportExemptAmount]
            ,[commissionRate]
            ,[commissionNetAmount]
            ,[commissionTaxAmount]
            ,[commissionTotalAmount]
            ,[percentageTaxWithheld]
            ,[purchaseTaxAmount]
            ,[purchaseTotalAmount]
            ,[address]
            ,[municipality]
            ,[city]
            ,[urlTimbre]
            ,[urlPublicView]
            ,[urlPdf]
            ,[urlPublicViewOriginal]
            ,[urlPdfOriginal]
            ,[token]
            ,[state]
            ,[urlXml]
            ,[informedSii]
            ,[responseMsgSii]
            ,[idTipoDocumento]
            ,[idClient]
            ,[idSucursal]
            ,[idUsuario]
            ,[details]
            ,[sellers]
            ,[attributes])
        VALUES
        """
    def setDocumentData(self,current):
        client='null'
        if "client" in current:
            client=current["client"]["id"]
        return f"""
            ({current["id"]}
           ,{current["emissionDate"]}
           ,{current["expirationDate"]}
           ,{current["generationDate"]}
           ,{current["number"]}
           ,{current["serialNumber"]}
           ,{current["totalAmount"]}
           ,{current["netAmount"]}
           ,{current["taxAmount"]}
           ,{current["exemptAmount"]}
           ,{current["notExemptAmount"]}
           ,{current["exportTotalAmount"]}
           ,{current["exportNetAmount"]}
           ,{current["exportTaxAmount"]}
           ,{current["exportExemptAmount"]}
           ,{current["commissionRate"]}
           ,{current["commissionNetAmount"]}
           ,{current["commissionTaxAmount"]}
           ,{current["commissionTotalAmount"]}
           ,{current["percentageTaxWithheld"]}
           ,{current["purchaseTaxAmount"]}
           ,{current["purchaseTotalAmount"]}
           ,'{current["address"]}'
           ,'{current["municipality"]}'
           ,'{current["city"]}'
           ,'{current["urlTimbre"]}'
           ,'{current["urlPublicView"]}'
           ,'{current["urlPdf"]}'
           ,'{current["urlPublicViewOriginal"]}'
           ,'{current["urlPdfOriginal"]}'
           ,'{current["token"]}'
           ,{current["state"]}
           ,'{current["urlXml"]}'
           ,{current["informedSii"]}
           ,'{current["responseMsgSii"]}'
           ,{current["document_type"]["id"]}
           ,{client}
           ,{current["office"]["id"]}
           ,{current["user"]["id"]}
           ,'{current["details"]["href"]}'
           ,'{current["sellers"]["href"]}'
           ,'{current["attributes"]["href"]}'),"""
    def setDetailDefault(self):
        return f"""
            INSERT INTO {self.detail}
                 ([id]
                ,[line]
                ,[quantity]
                ,[netUnitValue]
                ,[totalUnitValue]
                ,[netAmount]
                ,[taxAmount]
                ,[totalAmount]
                ,[netDiscount]
                ,[totalDiscount]
                ,[idVariante]
                ,[descriptionVariante]
                ,[codeVariante]
                ,[note]
                ,[relatedDetailId]
                ,[idDocumento])
            VALUES
        """
    def getDetalleData(self,current,document):
        return f"""
            ({current["id"]}
           ,{current["lineNumber"]}
           ,{current["quantity"]}
           ,{current["netUnitValue"]}
           ,{current["totalUnitValue"]}
           ,{current["netAmount"]}
           ,{current["taxAmount"]}
           ,{current["totalAmount"]}
           ,{current["netDiscount"]}
           ,{current["totalDiscount"]}
           ,{current["variant"]["id"]}
           ,'{current["variant"]["description"]}'
           ,'{current["variant"]["code"]}'
           ,'{current["note"]}'
           ,{current["relatedDetailId"]}
           ,{document}),"""
    def setVendedordata(self,data,documento):
        return f"""
            ({data["id"]}
           ,'{data["firstName"]}'
           ,'{data["lastName"]}'
           ,{documento}),"""


    def getInsertQuery(self):
        inicio=datetime.now()
        query=self.setDocumentDefault() 
        detailQuery=self.setDetailDefault()
        i=0
        contDetail=0
        documentDelete='delete from '+self.table+' where id in (0'
        vendedorDelete="delete from "+tablas["vendedor"]+ " where idDocumento in (0"
        vendedorQuery=self.setVendedorDefault()
        count=0
        for current in self.datas:
            i=i+1
            count=count+1
            print("documento",count)
            query=query+self.setDocumentData(current)
            vendedorDelete=vendedorDelete+','+str(current["id"])
            documentDelete=documentDelete+','+str(current["id"])
            vendedorQuery=vendedorQuery+self.setVendedordata(current["sellers"]["items"][0],current["id"])
            #eliminar detalle documento
            self.executeQuery("delete from "+self.detail+ " where idDocumento="+str(current["id"]))
            for detail in current["details"]["items"]:
                print("procesando detalle")
                contDetail=contDetail+1
                detailQuery=detailQuery+self.getDetalleData(detail,current["id"])
                if contDetail>900:
                    print(datetime.now()-inicio)
                    contDetail=0
                    detailQuery=detailQuery[:-1]
                    detailQuery.replace("'None'",'null')
                    query=query.replace('None','null')
                    #print(detailQuery)
                    print("Ingresando 900 detalles")
                    self.executeQuery(detailQuery)
                    detailQuery=self.setDetailDefault()
            if i>900:
                i=0
                documentDelete=documentDelete+")"
                self.executeQuery(documentDelete)
                vendedorDelete=vendedorDelete+')'
                self.executeQuery(vendedorDelete)
                documentDelete='delete from '+self.table+' where id in (0'
                vendedorDelete="delete from "+tablas["vendedor"]+ " where idDocumento in (0"
                file=open("testVendedor.txt","w")
                file.write(vendedorDelete)
                file.close()

                vendedorQuery=vendedorQuery.replace("'None'",'null')
                vendedorQuery=vendedorQuery.replace('None','null')
                vendedorQuery=vendedorQuery[:-1]
                self.executeQuery(vendedorQuery)                
                vendedorQuery=self.setVendedorDefault()
                
                query=query.replace("'None'",'null')
                query=query.replace('None','null')
                query=query[:-1]                
                print("Ingresando 900 documentos")
                self.executeQuery(query)
                print(datetime.now()-inicio)
                query=self.setDocumentDefault()

        vendedorQuery=vendedorQuery.replace("'None'",'null')
        vendedorQuery=vendedorQuery.replace('None','null')
        vendedorQuery=vendedorQuery[:-1]
        query=query.replace("'None'",'null')
        query=query.replace('None','null')
        query=query[:-1]
        documentDelete=documentDelete+")"
        self.executeQuery(vendedorQuery)                
        self.executeQuery(documentDelete)
        self.executeQuery(query)
        detailQuery=detailQuery[:-1]
        detailQuery.replace("'None'",'null')
        query=query.replace('None','null')
        self.executeQuery(detailQuery)
        detailQuery=self.setDetailDefault()
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def getDocument(self):
        file=open("documentosProblema.txt",'w')
        documents=[812,994,962,998,796,791,803,993,796,797,790,812,799,993,947,811,810,1047,994,998,998,946]
        for currentDocument in documents:
            try:
                url = os.getenv('API_URL_BASE') + '/'+str(currentDocument)+'/documents.json?limit=50&offset=0&expand=[details,sellers]'
            #1676430000.0 , 1678158000.0
                flag=True
                headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
                while(flag):
                    req = requests.get(url, headers=headers)
                    response=json.loads(req.text)
                    print(url)
                    if("next" in response):
                        flag=True
                        url=response["next"]+'&emissiondaterange=['+str(self.inicio)+' ,'+str(self.fin)+']&expand=[details,sellers]'
                    else:
                        flag=False
                    print(response)
                    if "items in response":
                        for current in response["items"]:
                            self.datas.append(current)
                    self.getInsertQuery()
            except:
                file.write(str(currentDocument)+' url '+url+'\n')
                print(currentDocument, url)
    
    def executelogic(self):
        print("Limpiando Documentos")
#        self.executeQuery(self.cleanData())
        print("Obteniendo documentos")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
#        self.executeQuery(query)]\
    def patchDocument(self):
        conn=ConnectionHandler()
        conn.connect()
        query=self.getNoDocument()
        result=conn.executeQuery(query)
        docs=[]
        for current in result:
#            docs.append(current)
            #limpiar datos actuales de detalle y vendedor
#            queryDetails="delete from "+tablas['detalleDocumento'] + " where idDocumento="+str(current[0])
 #           querySeller="delete from "+tablas['vendedor'] + " where idDocumento="+str(current[0])
  #          conn.executeQuery(queryDetails)
   #         conn.executeQuery(querySeller)
            data=self.getDataPatch(current[0])
            docs.append(data)
     #       print(data['number'])
            #Ingresar documento
            #ingresar detalles
            #ingresar vendedor
            #print(current[0]+"\\n"+queryDetails+"\\n"+querySeller)
        self.datas=docs
        self.getInsertQuery()
    def getNoDocument(self):
        return f'''
        

        select
            distinct venta.[Numero Documento] as number
        from BOT_VENTAS_SUCURSAL as venta
        left join DOCUMENTO as doc
            on doc.number=venta.[Numero Documento] 
        left join dbo.Detalle_Documento as detalle
            on detalle.idDocumento = doc.id  and detalle.codeVariante=venta.sku		
        left join VARIANTE 
            on Variante.id= detalle.idVariante 
        left join dbo.Producto
            on producto.id = Variante.idProducto
        left join dbo.Tipo_Producto as tipoProducto
            on tipoProducto.id = Producto.idTipoProducto
        left join dbo.Sucursal 
            on Sucursal.id = doc.idSucursal
        left join dbo.Tipo_Documento as TD 
            on TD.id = doc.idTipoDocumento
        left join dbo.VENDEDOR as VD 
            on VD.idDocumento = doc.id
        left join dbo.DETALLE_LISTA_PRECIO as DLP on DLP.idVariante = Variante.id
        left join dbo.LISTA_PRECIO as LP on  LP.id = DLP.idListaPrecio
        --left join BOT_VENTAS_SUCURSAL_CLEAN as venta on  venta.[Numero Documento]  = D.number   
        left join dbo.DEVOLUCION as Dv on DV.idDocumentoCredito = doc.id
        where (LP.name like '%base%' or Lp.id is null)
        and doc.id is null
        
        '''
    def getDataPatch(self,number):
        url = os.getenv('API_URL_BASE') + '/documents.json?number='+str(number)+'&expand=[details,sellers]'
        #1676430000.0 , 1678158000.0
        flag=True
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        req = requests.get(url, headers=headers)
        response=json.loads(req.text)
        print(url)
        result=None
        if "items in response":
            for current in response["items"]:
                result=current
        return result
