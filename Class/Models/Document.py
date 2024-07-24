class Document:
    def __init__(self,id,emissionDate,expirationDate,generationDate,number,serialNumber,totalAmount,netAmount,taxAmount,exemptAmount,notExemptAmount,exportTotalAmount,exportNetAmount,exportTaxAmount,exportExemptAmount,commissionRate,commissionNetAmount,commissionTaxAmount,commissionTotalAmount,percentageTaxWithheld,purchaseTaxAmount,purchaseTotalAmount,address,municipality,city,urlTimbre,urlPublicView,urlPdf,urlPublicViewOriginal,urlPdfOriginal,token,state,urlXml,informedSii,responseMsgSii,idTipoDocumento,idClient,idSucursal,idUsuario,details,sellers,attributes) -> None:
        self.id=id
        self.emissionDate=emissionDate
        self.expirationDate=expirationDate
        self.generationDate=generationDate
        self.number=number
        self.serialNumber=serialNumber
        self.totalAmount=totalAmount
        self.netAmount=netAmount
        self.taxAmount=taxAmount
        self.exemptAmount=exemptAmount
        self.notExemptAmount=notExemptAmount
        self.exportTotalAmount=exportTotalAmount
        self.exportNetAmount=exportNetAmount
        self.exportTaxAmount=exportTaxAmount
        self.exportExemptAmount=exportExemptAmount
        self.commissionRate=commissionRate
        self.commissionNetAmount=commissionNetAmount
        self.commissionTaxAmount=commissionTaxAmount
        self.commissionTotalAmount=commissionTotalAmount
        self.percentageTaxWithheld=percentageTaxWithheld
        self.purchaseTaxAmount=purchaseTaxAmount
        self.purchaseTotalAmount=purchaseTotalAmount
        self.address=address
        self.municipality=municipality
        self.city=city
        self.urlTimbre=urlTimbre
        self.urlPublicView=urlPublicView
        self.urlPdf=urlPdf
        self.urlPublicViewOriginal=urlPublicViewOriginal
        self.urlPdfOriginal=urlPdfOriginal
        self.token=token
        self.state=state
        self.urlXml=urlXml
        self.informedSii=informedSii
        self.responseMsgSii=responseMsgSii
        self.idTipoDocumento=idTipoDocumento
        self.idClient=idClient
        self.idSucursal=idSucursal
        self.idUsuario=idUsuario
        self.details=details
        self.sellers=sellers
        self.attributes=attributes
        
    def updateOrCreate():
        pass
    def getUpdateQuery(self):
        pass
    def getInsertQuery(self):
        pass
    def getDeleteDocument(self):
        pass