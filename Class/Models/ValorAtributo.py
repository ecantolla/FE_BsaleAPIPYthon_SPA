from Class.Models.tablas import tablas
from Class.ConnectionHandler import ConnectionHandler
class ValotAtributo:
    def __init__(self,id,description,idAtributo,idVariante) -> None:
        self.id=id
        self.description=description
        self.idAtributo=idAtributo
        self.idVariante=idVariante
        self.con=ConnectionHandler()

    def save(self):
        query=f"""
            INSERT INTO {tablas["valorAtributo"]}
                ([id]
                ,[description]
                ,[idAtributo]
                ,[idVariante])
            VALUES
                ({self.id}
                ,'{self.description}'
                ,{self.idAtributo}
                ,{self.idVariante})
        """
        self.con.connect()
        self.con.executeQuery(query)
        self.con.commitChange()
