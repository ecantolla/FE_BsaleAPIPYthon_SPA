from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class TipoProducto:
    def __init__(self,id,name,isEditable,state,imagestionCategoryId,prestashopCategoryId,attributos):
        self.id=id
        self.name=name
        self.isEditable=isEditable
        self.state=state
        self.imagestionCategoryId=imagestionCategoryId
        self.prestashopCategoryId=prestashopCategoryId
        self.attributos=attributos
        self.con=ConnectionHandler()
    def createOrUpdate(self):
        query="select * from "+tablas["tipoProducto"]+" where id="+str(self.id)
        self.con.connect()
        result=self.con.executeQuery(query)
        
        if(len(result.fetchall())==0):
            queryAction=self.getInsertQuery()
        else:
            queryAction=self.getUpdateQuery()
        
        self.con.executeQuery(queryAction)
        self.con.commitChange()
        #eliminar los registros del tipo de producto
        queryAction="delete from "+tablas["atributo"]+" where idTipoProducto="+str(self.id)
        self.con.executeQuery(queryAction)
        self.con.commitChange()
        #ir por los atributos de un tipo de producto
        
        headers = {'Accept': 'application/json','access_token':os.getenv('API_KEY')}
        req = requests.get(self.attributos, headers=headers)
        response=json.loads(req.text)
        if(response["count"]>0):
            for item in response["items"]:     
                query=f"""
                INSERT INTO {tablas["atributo"]}
                    ([id]
                    ,[name]
                    ,[isMandatory]
                    ,[generateVariantName]
                    ,[hasOptions]
                    ,[options]
                    ,[state]
                    ,[idTipoProducto])
                VALUES
                    ({item["id"]}
                    ,'{item["name"]}'
                    ,{item["isMandatory"]}
                    ,{item["generateVariantName"]}
                    ,{item["hasOptions"]}
                    ,'{item["options"]}'
                    ,{item["state"]}
                    ,{self.id})
                """
                self.con.executeQuery(query)
                self.con.commitChange()
        
        
        
    def getUpdateQuery(self):
        print("generando query update")
        return f"""
        UPDATE {tablas["tipoProducto"]}
        SET 
        [name] = '{self.name}'
        ,[isEditable] = {self.isEditable}
        ,[state] = {self.state}
        ,[imagestionCategoryId] = {self.imagestionCategoryId}
        ,[prestashopCategoryId] = {self.prestashopCategoryId}
        ,[attributos] = '{self.attributos}'
         WHERE [id]={self.id}"""
    def getInsertQuery(self):
        print("generando query insert")
        return f"""
        INSERT INTO {tablas["tipoProducto"]}
           ([id]
           ,[name]
           ,[isEditable]
           ,[state]
           ,[imagestionCategoryId]
           ,[prestashopCategoryId]
           ,[attributos])
     VALUES
           ({self.id}
           ,'{self.name}'
           ,{self.isEditable}
           ,{self.state}
           ,{self.imagestionCategoryId}
           ,{self.prestashopCategoryId}
           ,'{self.attributos}')
        """
