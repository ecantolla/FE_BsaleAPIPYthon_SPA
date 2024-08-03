import numpy as np

from Class.Controller.AbstractController import AbstractController
from Class.Controller.Herlpers import get_col_dtype, format_record
from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class DocumentoController(AbstractController):
    def __init__(self, tabla):
        super().__init__(tabla)
        self.table2 = tablas["vendedor"]
        c_t2 = np.array([ct for ct in get_col_dtype(self.table2)])
        self.table2_cols = c_t2[:, 0].tolist()
        self.table2_ctypes = c_t2[:, 1].tolist()
        self.table2_datas = []
        self.table3 = tablas["detalleDocumento"]
        c_t3 = np.array([ct for ct in get_col_dtype(self.table3)])
        self.table3_cols = c_t3[:, 0].tolist()
        self.table3_ctypes = c_t3[:, 1].tolist()
        self.table3_datas = []
        now = datetime.now()
        self.inicio = now - relativedelta(months=6)
        self.inicio = int(self.inicio.timestamp())
        self.fin = int(now.timestamp())
        self.doc_ids = []
        
    def clear_table(self, table=None):
        tbl = self.table if table is None else table
        id_field = '[id]' if table is None else '[idDocumento]'
        query = f"DELETE FROM {tbl} where {id_field} in "
        query += '(' + ','.join(self.doc_ids) + ');'
        self.execute_query(query, "delete")

    def get_data(self):
        params = f"&expand=[details,sellers]&emissiondaterange=[{self.inicio},{self.fin}]"
        url = os.getenv('API_URL_BASE') + "/documents.json?limit=50&offset=0" + params
        headers = {'Accept': 'application/json', 'access_token': os.getenv('API_KEY')}
        while True:
            req = requests.get(url, headers=headers)
            response = json.loads(req.text)
            for current in response["items"]:
                self.doc_ids.append(str(current["id"]))

                for detail in current["details"]["items"]:
                    detail["idDocumento"] = current["id"]
                    detail["line"] = detail["lineNumber"]
                    detail["idVariante"] = detail["variant"]["id"]
                    detail["descriptionVariante"] = detail["variant"]["description"]
                    detail["codeVariante"] = detail["variant"]["code"]
                    detail = format_record(detail, self.table3_cols, self.table3_ctypes)
                    self.table3_datas.append(detail)

                vend = current["sellers"]["items"][0]
                vend["idUsuario"] = vend["id"]
                vend["idDocumento"] = current["id"]
                vend = format_record(vend, self.table2_cols, self.table2_ctypes)
                self.table2_datas.append(vend)

                current['idTipoDocumento'] = current["document_type"]["id"]
                current['idClient'] = current["client"]["id"] if 'client' in current else None
                current['idSucursal'] = current["office"]["id"]
                current['idUsuario'] = current["user"]["id"]
                current['details'] = current["details"]["href"]
                current['sellers'] = current["sellers"]["href"]
                current['attributes'] = current["attributes"]["href"]
                current = format_record(current, self.cols, self.ctypes)
                self.datas.append(current)

            if "next" in response:
                url = response["next"] + params
            else:
                break

    def insert_data(self):
        query = f'INSERT INTO {self.table} '
        query += '(' + ','.join([f'[{c}]' for c in self.cols]) + ')'
        query += ' VALUES (' + ','.join(['?' for c in range(len(self.cols))]) + ')'
        values = []
        for i, current in enumerate(self.datas, 1):
            vals = tuple([current[c] for c in self.cols])
            values.append(vals)
            if i % 900 == 0:
                print(f"insertando documento {i}")
                self.execute_query(query, 'insert', values)
                values = []
        if values:
            print(f"insertando documento")
            self.execute_query(query, 'insert', values)

        vend_query = f'INSERT INTO {self.table2} '
        vend_query += '(' + ','.join([f'[{c}]' for c in self.table2_cols]) + ')'
        vend_query += f' VALUES (' + ','.join(['?' for c in range(len(self.table2_cols))]) + ')'
        vend_values = []
        for i, current in enumerate(self.table2_datas, 1):
            vals = tuple([current[c] for c in self.table2_cols])
            vend_values.append(vals)
            if i % 900 == 0:
                print(f"insertando vendedor {i}")
                self.execute_query(vend_query, 'insert', vend_values)
                vend_values = []
        if vend_values:
            print(f"insertando vendedores")
            self.execute_query(vend_query, 'insert', vend_values)

        detail_query = f'INSERT INTO {self.table3} '
        detail_query += '(' + ','.join([f'[{c}]' for c in self.table3_cols]) + ')'
        detail_query += f' VALUES (' + ','.join(['?' for c in range(len(self.table3_cols))]) + ')'
        detail_values = []
        for i, current in enumerate(self.table3_datas, 1):
            vals = tuple([current[c] for c in self.table3_cols])
            detail_values.append(vals)
            if i % 900 == 0:
                print(f"insertando detalle {i}")
                self.execute_query(detail_query, 'insert', detail_values)
                detail_values = []
        if detail_values:
            print(f"insertando detalle")
            self.execute_query(detail_query, 'insert', detail_values)

    def execute_logic(self):
        print("Obteniendo documentos")
        self.get_data()
        print("Limpiando Documentos")
        self.clear_table()
        self.clear_table(self.table2)
        self.clear_table(self.table3)
        print("Generando Query")
        self.insert_data()

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

    def patchDocument(self):
        conn=ConnectionHandler()
        conn.connect()
        query=self.getNoDocument()
        result=conn.executeQuery(query)
        docs=[]
        for current in result:
            # docs.append(current)
            # limpiar datos actuales de detalle y vendedor
            # queryDetails="delete from "+tablas['detalleDocumento'] + " where idDocumento="+str(current[0])
            # querySeller="delete from "+tablas['vendedor'] + " where idDocumento="+str(current[0])
            # conn.executeQuery(queryDetails)
            # conn.executeQuery(querySeller)
            data = self.getDataPatch(current[0])
            docs.append(data)

        self.datas = docs
        self.insert_data()
