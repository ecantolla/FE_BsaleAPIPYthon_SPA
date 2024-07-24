from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler

class ListaPrecio:
    def __init__(self,id,name,description,state,details) -> None:
        self.id=id
        self.name=name
        self.description=description
        self.state=state
        self.details=details
        self.con=ConnectionHandler()
    def save(self):
        query=f"""
            INSERT INTO {tablas["listaPrecio"]}
                ([id]
                ,[name]
                ,[description]
                ,[state]
                ,[details])
            VALUES
                ({self.id}
                ,'{self.name}'
                ,'{self.description}'
                ,{self.state}
                ,'{self.details}')
        """
        self.con.connect()
        self.con.executeQuery(query)
        self.con.commitChange()
        