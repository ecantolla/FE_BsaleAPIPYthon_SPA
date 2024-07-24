from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas,updateTipoDocumento,createTipoDocumento
class TipoDocumento:
    def __init__(self,id,name,initialNumber,codeSii,isElectronicDocument,breakdownTax,use,isSalesNote,isExempt,restrictsTax,useClient,thermalPrinter,state,copyNumber,isCreditNote,continuedHigh,ledgerAccount,ipadPrint,ipadPrintHigh,restrictClientType,idTipoLibro):
        self.id=id
        self.name=name
        self.initialNumber=initialNumber
        self.codeSii=codeSii
        self.isElectronicDocument=isElectronicDocument
        self.breakdownTax=breakdownTax
        self.use=use
        self.isSalesNote=isSalesNote
        self.isExempt=isExempt
        self.restrictsTax=restrictsTax
        self.useClient=useClient
        self.thermalPrinter=thermalPrinter
        self.state=state
        self.copyNumber=copyNumber
        self.isCreditNote=isCreditNote
        self.continuedHigh=continuedHigh
        self.ledgerAccount=ledgerAccount
        self.ipadPrint=ipadPrint
        self.ipadPrintHigh=ipadPrintHigh
        self.restrictClientType=restrictClientType
        self.idTipoLibro=idTipoLibro
        self.con=ConnectionHandler()
    def updateOrCreate(self):
        #Buscar en la tabla si existe el registro
        print(tablas["tipoDocumento"])
        query="select * from "+tablas["tipoDocumento"]+" where id="+str(self.id)
        self.con.connect()
        result=self.con.executeQuery(query)
        status=False
        for current in result:
            query=updateTipoDocumento(self.id,self.name,self.initialNumber,self.codeSii,self.isElectronicDocument,self.breakdownTax,self.use,self.isSalesNote,self.isExempt,self.restrictsTax,self.useClient,self.thermalPrinter,self.state,self.copyNumber,self.isCreditNote,self.continuedHigh,self.ledgerAccount,self.ipadPrint,self.ipadPrintHigh,self.restrictClientType,self.idTipoLibro)
            status=True
        if(status==False):
            query=createTipoDocumento(self.id,self.name,self.initialNumber,self.codeSii,self.isElectronicDocument,self.breakdownTax,self.use,self.isSalesNote,self.isExempt,self.restrictsTax,self.useClient,self.thermalPrinter,self.state,self.copyNumber,self.isCreditNote,self.continuedHigh,self.ledgerAccount,self.ipadPrint,self.ipadPrintHigh,self.restrictClientType,self.idTipoLibro)
        self.con.executeQuery(query)
        self.con.commitChange()
        return self.id        
    def clean(self,tpList):
        query="delete from  "+ tablas["tipoDocumento"]+" where id not in"+tpList
        self.con.connect()
        self.con.executeQuery(query)
        self.con.commitChange()
        

