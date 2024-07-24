from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
import requests
import json

class VarianteController:
    def __init__(self):
        self.table=tablas["variante"]
        self.productTable=tablas["producto"]
        self.attTable=tablas["valorAtributo"]
        self.datas=[]
    def cleanData(self):
        query=f"""delete from {self.table}"""
        self.executeQuery("delete from "+ self.attTable)
        self.executeQuery("delete from "+self.productTable)

        return query
    def getData(self):
        url = 'https://api.bsale.cl/v1/variants.json?expand=[attribute_values,product,costs]&limit=50&offset=0'
        flag=True
        headers = {'Accept': 'application/json','access_token':'6de4c01b2a3d7f64153f0e4f96b1c1f51218be56'}
        i=0
        while(flag):
            req = requests.get(url, headers=headers)
            response=json.loads(req.text)
            print(url)
            if("next" in response):
                flag=True
                i=i+1
                url=response["next"]+'&expand=[attribute_values,product,costs]'
                """ if(i>30):
                    flag=False """
            else:
                flag=False
            if "items" in response:
                for current in response["items"]:
                    self.datas.append(current)
    def getInsertQuery(self):
        query=f"""
        INSERT INTO {self.table}
                ([id]
                ,[description]
                ,[unlimitedStock]
                ,[allowNegativeStock]
                ,[state]
                ,[barCode]
                ,[code]
                ,[imagestionCenterCost]
                ,[imagestionAccount]
                ,[imagestionConceptCod]
                ,[imagestionProyectCod]
                ,[imagestionCategoryCod]
                ,[imagestionProductId]
                ,[serialNumber]
                ,[prestashopCombinationId]
                ,[prestashopValueId]
                ,[idProducto]
                ,[atributos]
                ,[costos]
                ,[costoPromedio])
            VALUES
            """
        products=[]
            
        attQuery=f"""
            INSERT INTO {self.attTable}
                ([id]
                ,[description]
                ,[idAtributo]
                ,[idVariante])
                VALUES
                """
        
        productQuery=f"""
                INSERT INTO {self.productTable}
                    ([id]
                    ,[name]
                    ,[description]
                    ,[classification]
                    ,[ledgerAccount]
                    ,[costCenter]
                    ,[allowDecimal]
                    ,[stockControl]
                    ,[printDetailPack]
                    ,[state]
                    ,[prestashopProductId]
                    ,[presashopAttributeId]
                    ,[idTipoProducto])
                VALUES
                """
        contAtt=0
        contProduct=0
        contVariante=0
        for current in self.datas:
            #eliminar los productos
            contVariante=contVariante+1
            avg=0
            if "costs" in current:
                if "averageCost" in current["costs"]:
                    avg=current["costs"]["averageCost"]
            
            query=query+f"""
                ({current["id"]}
                ,'{current["description"]}'
                ,{current["unlimitedStock"]}
                ,{current["allowNegativeStock"]}
                ,{current["state"]}
                ,'{current["barCode"].replace("'","")}'
                ,'{current["code"]}'
                ,{current["imagestionCenterCost"]}
                ,{current["imagestionAccount"]}
                ,{current["imagestionConceptCod"]}
                ,{current["imagestionProyectCod"]}
                ,{current["imagestionCategoryCod"]}
                ,{current["imagestionProductId"]}
                ,{current["serialNumber"]}
                ,{current["prestashopCombinationId"]}
                ,{current["prestashopValueId"]}
                ,{current["product"]["id"]}
                ,'{current["attribute_values"]["href"]}'
                ,'https://api.bsale.cl/v1/variants/{current["id"]}/costs.json'
                ,{avg}),"""
            if(contVariante>900):
                contVariante=0
                query=query.replace("'None'",'null')
                query=query[:-1]
                self.executeQuery(query)
                query=f"""
                    INSERT INTO {self.table}
                            ([id]
                            ,[description]
                            ,[unlimitedStock]
                            ,[allowNegativeStock]
                            ,[state]
                            ,[barCode]
                            ,[code]
                            ,[imagestionCenterCost]
                            ,[imagestionAccount]
                            ,[imagestionConceptCod]
                            ,[imagestionProyectCod]
                            ,[imagestionCategoryCod]
                            ,[imagestionProductId]
                            ,[serialNumber]
                            ,[prestashopCombinationId]
                            ,[prestashopValueId]
                            ,[idProducto]
                            ,[atributos]
                            ,[costos]
                            ,[costoPromedio])
                        VALUES
                        """
            #agregar producto
            if current["product"]["id"] not in products:
                products.append(current["product"]["id"])
                contProduct=contProduct+1
                productQuery=productQuery+f"""
                    ({current["product"]["id"]}
                    ,'{current["product"]["name"]}'
                    ,'{current["product"]["description"]}'
                    ,{current["product"]["classification"]}
                    ,'{current["product"]["ledgerAccount"]}'
                    ,'{current["product"]["costCenter"]}'
                    ,{current["product"]["allowDecimal"]}
                    ,{current["product"]["stockControl"]}
                    ,{current["product"]["printDetailPack"]}
                    ,{current["product"]["state"]}
                    ,{current["product"]["prestashopProductId"]}
                    ,{current["product"]["presashopAttributeId"]}
                    ,{current["product"]["product_type"]["id"]}),"""
                if contProduct>900:
                    contProduct=0
                    productQuery=productQuery[:-1]
                    self.executeQuery(productQuery)
                    productQuery=f"""
                        INSERT INTO {self.productTable}
                            ([id]
                            ,[name]
                            ,[description]
                            ,[classification]
                            ,[ledgerAccount]
                            ,[costCenter]
                            ,[allowDecimal]
                            ,[stockControl]
                            ,[printDetailPack]
                            ,[state]
                            ,[prestashopProductId]
                            ,[presashopAttributeId]
                            ,[idTipoProducto])
                        VALUES
                        """            
            #eliminar los atributos
            for att in current["attribute_values"]["items"]:
                contAtt=contAtt+1

                atrdescription = att["description"]
                if atrdescription:
                    atrdescription = atrdescription.replace("'", "''")

                attQuery=attQuery+f"""        
                    ({att["id"]}
                    ,'{atrdescription}'
                    ,{att["attribute"]["id"]}
                    ,{current["id"]}),"""
                if contAtt>900:
                    contAtt=0
                    attQuery=attQuery[:-1]
                    #attQuery=attQuery.replace("L'OREAL","LOREAL")
                    #attQuery=attQuery.replace("L'Oreal","L''Oreal")
                    self.executeQuery(attQuery)
                    attQuery=f"""
                        INSERT INTO {self.attTable}
                            ([id]
                            ,[description]
                            ,[idAtributo]
                            ,[idVariante])
                            VALUES
                            """        
        productQuery=productQuery[:-1]
        print("producto")
        
        self.executeQuery(productQuery)
        #attQuery=attQuery.replace("L'OREAL","LOREAL")
        #attQuery=attQuery.replace("L'Oreal","L''Oreal")
        attQuery=attQuery[:-1]
        print("atributo")
        att=open('Atributos.txt','w')
        att.write(attQuery)
        self.executeQuery(attQuery)
        query=query.replace("'None'",'null')
        query=query[:-1]
        print("variante")
        file=open("test.txt","w")
        file.write(productQuery)
        file.close()
        self.executeQuery(query)
        return query
    def executeQuery(self,query):
        conn=ConnectionHandler()
        conn.connect()
        conn.executeQuery(query)
        conn.commitChange()
        conn.closeConnection()
    def executelogic(self):
        print("Limpiando variante")
        self.executeQuery(self.cleanData())
        print("Obteniendo variante")
        self.getData()
        print("Generando Query")
        query=self.getInsertQuery()
        # self.executeQuery(query)