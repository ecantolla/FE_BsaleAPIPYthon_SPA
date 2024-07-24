from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas
import requests
import json
from datetime import datetime
class Producto:
    def __init__(self,id,name,description,classification,ledgerAccount,costCenter,allowDecimal,stockControl,printDetailPack,state,prestashopProductId,presashopAttributeId,idTipoProducto,variante):
        self.id=id
        self.name=name
        self.description=description
        self.classification=classification
        self.ledgerAccount=ledgerAccount
        self.costCenter=costCenter
        self.allowDecimal=allowDecimal
        self.stockControl=stockControl
        self.printDetailPack=printDetailPack
        self.state=state
        self.prestashopProductId=prestashopProductId
        self.presashopAttributeId=presashopAttributeId
        self.idTipoProducto=idTipoProducto
        self.con=ConnectionHandler()
        self.variante=variante
    def createOrUpdate(self):
        currentTime=datetime.now()
        query="select * from "+tablas["producto"]+" where id="+str(self.id)
        print(query)
        self.con.connect()
        queryAction=self.getInsertQuery()
        self.con.executeQuery(queryAction)
        self.con.commitChange()        
        print(datetime.now()-currentTime)
        
    def getInsertQuery(self):
        print("generando insert query")
        return f"""
        INSERT INTO {tablas["producto"]}
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
                ({self.id}
                ,'{self.name}'
                ,'{self.description}'
                ,{self.classification}
                ,'{self.ledgerAccount}'
                ,'{self.costCenter}'
                ,{self.allowDecimal}
                ,{self.stockControl}
                ,{self.printDetailPack}
                ,{self.state}
                ,{self.prestashopProductId}
                ,{self.presashopAttributeId}
                ,{self.idTipoProducto})
        """
    def getUpdateQuery(self):
        print("generando update query")
        return f"""
            UPDATE {tablas["producto"]}
            SET 
                [name] = '{self.name}'
                ,[description] = '{self.description}'
                ,[classification] = {self.classification}
                ,[ledgerAccount] = '{self.ledgerAccount}'
                ,[costCenter] = '{self.costCenter}'
                ,[allowDecimal] = {self.allowDecimal}
                ,[stockControl] = {self.stockControl}
                ,[printDetailPack] = {self.printDetailPack}
                ,[state] = {self.state}
                ,[prestashopProductId] = {self.prestashopProductId}
                ,[presashopAttributeId] = {self.presashopAttributeId}
                ,[idTipoProducto] = {self.idTipoProducto}
            WHERE [id]={self.id}
        """
