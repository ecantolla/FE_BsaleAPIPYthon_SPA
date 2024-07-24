from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas

class Variante:
    def __init__(self,id,description,unlimitedStock,allowNegativeStock,state,barCode,code,imagestionCenterCost,imagestionAccount,imagestionConceptCod,imagestionProyectCod,imagestionCategoryCod,imagestionProductId,serialNumber,prestashopCombinationId,prestashopValueId,idProducto,atributos,costos,costoPromedio):
        self.id=id
        self.description=description
        self.unlimitedStock=unlimitedStock
        self.allowNegativeStock=allowNegativeStock
        self.state=state
        self.barCode=barCode
        self.code=code
        self.imagestionCenterCost=imagestionCenterCost
        self.imagestionAccount=imagestionAccount
        self.imagestionConceptCod=imagestionConceptCod
        self.imagestionProyectCod=imagestionProyectCod
        self.imagestionCategoryCod=imagestionCategoryCod
        self.imagestionProductId=imagestionProductId
        self.serialNumber=serialNumber
        self.prestashopCombinationId=prestashopCombinationId
        self.prestashopValueId=prestashopValueId
        self.idProducto=idProducto
        self.atributos=atributos
        self.costos=costos
        self.costoPromedio=costoPromedio
        self.con=ConnectionHandler()
        
    def save(self):
        self.con.connect()
        print("Registrando"+ str(self.id))
        queryAction=f"""
                        INSERT INTO {tablas["variante"]}
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
                        ({self.id}
                        ,'{self.description}'
                        ,{self.unlimitedStock}
                        ,{self.allowNegativeStock}
                        ,{self.state}
                        ,'{self.barCode}'
                        ,'{self.code}'
                        ,{self.imagestionCenterCost}
                        ,{self.imagestionAccount}
                        ,{self.imagestionConceptCod}
                        ,{self.imagestionProyectCod}
                        ,{self.imagestionCategoryCod}
                        ,{self.imagestionProductId}
                        ,{self.serialNumber}
                        ,{self.prestashopCombinationId}
                        ,{self.prestashopValueId}
                        ,{self.idProducto}
                        ,'{self.atributos}'
                        ,'{self.costos}'
                        ,{self.costoPromedio})
                    """
        self.con.executeQuery(queryAction)
        self.con.commitChange()