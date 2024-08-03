tablas = {
    "atributo": "atributo_aux",
    "cliente": "cliente",       # unico: field - code  #### MIGRADA v0 A v1
    "consumo": "consumo_aux",       # id needed: cl/io + current id
    "consumoDetalle": "detalle_consumo_aux",    # unico: field - id.
    "descuento": "descuento_aux",       # unico: field - id.
    "detalleListaPrecio": "DETALLE_LISTA_PRECIO_aux",       # unico: field - id.
    "detalle_devolucion": "detalle_devolucion_aux",     # unico: field - id.
    "detalleDocumento": "detalle_documento",        # unico: field - id. - idvariante,codevariante,iddocumento
    "devolucion": "devolucion_aux",         # unico: field - id ### [idOficina],[idUsuario],[idDocumentoReferencia],[idDocumentoCredito]
    "documento": "DOCUMENTO",       # no es unico pero tipo_documento lo es
    "listaPrecio": "lista_precio_aux",      # unico: field - id.    #### MIGRADA v0 A v1
    "producto": "PRODUCTO",     #### MIGRADA v0 A v1
    "recepcionDetalle": "recepcion_detalle_aux",    # la trae el BOT y RecepcionController inserta esta info a la DB
    "recepcion": "recepcion_aux",       # unico: field - id, ifOficina(Sucursal), idUsuario
    "stock": "stock",       # es un snapshot del dia
    "sucursal": "sucursal_aux",         # unico: field - id
    "tipoDocumento": "Tipo_Documento_aux",      # unico field - id. Aplica agregar sufijo cl por api antigua para id unico
    "tipoLibro": "tipoLibro_aux",       #### MIGRADA v0 A v1
    "tipoProducto": "tipo_producto",        # CATEG PROD. Y VARIANTE        #### MIGRADA v0 A v1
    "valorAtributo": "valor_atributo",      # unico: field - id - idAtributo,idVariante
    "variante": "variante",     # unico: field - id.
    "vendedor": "vendedor",
    "usuario": "usuario",       #### MIGRADA v0 A v1 - state 0/1 active/inactive
}

old_tablas = {
    "detalle_devolucion": "OLD1807_DETALLE_DEVOLUCION",
    "devolucion": "OLD1807_DEVOLUCION",
    "cliente": "OLD1807_CLIENTE",    
    "vendedor": "OLD1807_VENDEDOR",
    "documento": "OLD1807_DOCUMENTO",
    "detalleDocumento": "OLD1807_DETALLE_DOCUMENTO",
    "consumo": "OLD1807_CONSUMO",
    "consumoDetalle": "OLD1807_DETALLE_CONSUMO",
    "recepcionDetalle": "OLD1807_DETALLE_RECEPCION",
    "recepcion": "OLD1807_RECEPCION",
    "stock": "OLD1807_STOCK",
    "detalleListaPrecio": "OLD1807_DETALLE_LISTA_PRECIO",
    "listaPrecio": "OLD1807_LISTA_PRECIO",
    "valorAtributo": "OLD1807_VALOR_ATRIBUTO",
    "producto": "OLD1807_PRODUCTO",
    "variante": "OLD1807_VARIANTE",
    "atributo": "OLD1807_ATRIBUTO",
    "tipoProducto": "OLD1807_TIPO_PRODUCTO",
    "tipoDocumento": "OLD1807_TIPO_DOCUMENTO",
    "sucursal": "OLD1807_SUCURSAL",
    "usuario": "OLD1807_USUARIO",
    "descuento": "OLD1807_DESCUENTO",
    "tipoLibro": "OLD1807_TIPO_LIBRO"
}

#tablas={
#    "detalle_devolucion": "detalle_devolucion_aux",
#    "devolucion": "devolucion_aux",
#    "cliente": "cliente_aux",    
#    "vendedor": "vendedor",
#    "documento": "documento",
#    "detalleDocumento": "detalle_documento",
#    "consumo": "consumo_aux",
#    "consumoDetalle": "detalle_consumo_aux",
##    "recepcionDetalle": "recepcion_detalle_aux",
#    "recepcion": "recepcion_aux",
#    "stock": "stock",
#   "detalleListaPrecio": "DETALLE_LISTA_PRECIO_aux",
#  "listaPrecio": "lista_precio_aux",
# "valorAtributo": "valor_atributo",
#    "producto": "PRODUCTO",
#    "variante": "variante",
#    "atributo": "atributo_aux",
#    "tipoProducto": "tipo_producto",
#    "tipoDocumento": "Tipo_Documento_aux",
#    "sucursal": "sucursal_aux",
#    "usuario": "usuario_aux",
#    "descuento": "descuento_aux",
#    "tipoLibro": "tipoLibro_aux"
#}

def createSucursal(id,name,description,address,latitude,longitude,isVirtual,country,municipality,city,zipCode,email,costCenter,state,imagestionCellarId,defaultPriceList):
    return f"""
        INSERT INTO {tablas["sucursal"]}
           ([id]
           ,[name]
           ,[description]
           ,[address]
           ,[latitude]
           ,[longitude]
           ,[isVirtual]
           ,[country]
           ,[municipality]
           ,[city]
           ,[zipCode]
           ,[email]
           ,[costCenter]
           ,[state]
           ,[imagestionCellarId]
           ,[defaultPriceList])
     VALUES
           ({id}
           ,'{name}'
           ,'{description}'
           ,'{address}'
           ,'{latitude}'
           ,'{longitude}'
           ,{isVirtual}
           ,'{country}'
           ,'{municipality}'
           ,'{city}'
           ,'{zipCode}'
           ,'{email}'
           ,'{costCenter}'
           ,{state}
           ,{imagestionCellarId}
           ,{defaultPriceList})
    """
def updateSucursal(id,name,description,address,latitude,longitude,isVirtual,country,municipality,city,zipCode,email,costCenter,state,imagestionCellarId,defaultPriceList):
    return f"""
        UPDATE {tablas["sucursal"]}
   SET 
      [name] = '{name}'
      ,[description] = '{description}'
      ,[address] = '{address}'
      ,[latitude] = '{latitude}'
      ,[longitude] = '{longitude}'
      ,[isVirtual] = {isVirtual}
      ,[country] = '{country}'
      ,[municipality] = '{municipality}'
      ,[city] = '{city}'
      ,[zipCode] = '{zipCode}'
      ,[email] = '{email}'
      ,[costCenter] = '{costCenter}'
      ,[state] = {state}
      ,[imagestionCellarId] = {imagestionCellarId}
      ,[defaultPriceList] = {defaultPriceList}
 WHERE [id]={id}
    """

def updateTipoDocumento(id,name,initialNumber,codeSii,isElectronicDocument,breakdownTax,use,isSalesNote,isExempt,restrictsTax,useClient,thermalPrinter,state,copyNumber,isCreditNote,continuedHigh,ledgerAccount,ipadPrint,ipadPrintHigh,restrictClientType,idTipoLibro):
    bookTypeCurr=idTipoLibro
    if(bookTypeCurr==None):
        bookTypeCurr='null'
    return f"""
UPDATE [dbo].{tablas["tipoDocumento"]}
   SET 
      [name] = '{name}'
      ,[initialNumber] = {initialNumber}
      ,[codeSii] = '{codeSii}'
      ,[isElectronicDocument] = {isElectronicDocument}
      ,[breakdownTax] = {breakdownTax}
      ,[use] = {use}
      ,[isSalesNote] = {isSalesNote}
      ,[isExempt] = {isExempt}
      ,[restrictsTax] = {restrictsTax}
      ,[useClient] = {useClient}
      ,[thermalPrinter] = {thermalPrinter}
      ,[state] = {state}
      ,[copyNumber] = {copyNumber}
      ,[isCreditNote] = {isCreditNote}
      ,[continuedHigh] = {continuedHigh}
      ,[ledgerAccount] = '{ledgerAccount}'
      ,[ipadPrint] = {ipadPrint}
      ,[ipadPrintHigh] = {ipadPrintHigh}
      ,[restrictClientType] = {restrictClientType}
      ,[idTipoLibro] = {bookTypeCurr}
 WHERE [id]={id}
    """
def createTipoDocumento(id,name,initialNumber,codeSii,isElectronicDocument,breakdownTax,use,isSalesNote,isExempt,restrictsTax,useClient,thermalPrinter,state,copyNumber,isCreditNote,continuedHigh,ledgerAccount,ipadPrint,ipadPrintHigh,restrictClientType,idTipoLibro):
    bookTypeCurr=idTipoLibro
    if(bookTypeCurr==None):
        bookTypeCurr='null'
    return f"""INSERT INTO [dbo].[Tipo_Documento_aux]
           ([id]
           ,[name]
           ,[initialNumber]
           ,[codeSii]
           ,[isElectronicDocument]
           ,[breakdownTax]
           ,[use]
           ,[isSalesNote]
           ,[isExempt]
           ,[restrictsTax]
           ,[useClient]
           ,[thermalPrinter]
           ,[state]
           ,[copyNumber]
           ,[isCreditNote]
           ,[continuedHigh]
           ,[ledgerAccount]
           ,[ipadPrint]
           ,[ipadPrintHigh]
           ,[restrictClientType]
           ,[idTipoLibro])
     VALUES
           ({id}
           ,'{name}'
           ,{initialNumber}
           ,'{codeSii}'
           ,{isElectronicDocument}
           ,{breakdownTax}
           ,{use}
           ,{isSalesNote}
           ,{isExempt}
           ,{restrictsTax}
           ,{useClient}
           ,{thermalPrinter}
           ,{state}
           ,{copyNumber}
           ,{isCreditNote}
           ,{continuedHigh}
           ,'{ledgerAccount}'
           ,{ipadPrint}
           ,{ipadPrintHigh}
           ,{restrictClientType}
           ,{bookTypeCurr})"""
