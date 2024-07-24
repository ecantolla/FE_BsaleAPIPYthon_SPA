queries={
    "getCompras":"select distinct documento.id from BOT_VENTAS_SUCURSAL as bot inner join DOCUMENTO on bot.[Numero Documento]=documento.number left join VENDEDOR on Vendedor.idDocumento=DOCUMENTO.id where Vendedor.idUsuario is null and bot.[Fecha Documento] like ",
    "getDuplicado":"select 	distinct DOCUMENTO.number	,documento.id	,(select count(*) from vendedor where idDocumento=DOCUMENTO.id)	from BOT_VENTAS_SUCURSAL as bot inner join DOCUMENTO on bot.[Numero Documento]=documento.number where bot.[Fecha Documento] like ",
    "getDocumentoWithOutSeller":"select distinct [Numero Documento] from DetalleReporte where FechaDocumento2 like '2022/09%' and (idVendedor is null )",
    "getDocumentoNull":"select distinct venta.[Numero Documento] from BOT_VENTAS_SUCURSAL as venta left join DOCUMENTO as doc on doc.number=venta.[Numero Documento] where  doc.id is null and venta.[Fecha Documento]like ",
    "documentInsert":"INSERT INTO [dbo].[DOCUMENTO]([id],[emissionDate],[expirationDate],[generationDate],[number],[serialNumber],[totalAmount],[netAmount],[taxAmount],[exemptAmount],[notExemptAmount],[exportTotalAmount],[exportNetAmount],[exportTaxAmount],[exportExemptAmount],[commissionRate],[commissionNetAmount],[commissionTaxAmount],[commissionTotalAmount],[percentageTaxWithheld],[purchaseTaxAmount],[purchaseTotalAmount],[address],[municipality],[city],[urlTimbre],[urlPublicView],[urlPdf],[urlPublicViewOriginal],[urlPdfOriginal],[token],[state],[urlXml],[informedSii],[responseMsgSii],[idTipoDocumento],[idClient],[idSucursal],[idUsuario],[details],[sellers],[attributes])",
    "documentDetails":"select distinct doc.id,doc.details from BOT_VENTAS_SUCURSAL as venta left join DOCUMENTO as doc 	on doc.number=venta.[Numero Documento] left join dbo.Detalle_Documento as detalle 	on detalle.idDocumento = doc.id  and detalle.codeVariante=venta.sku	where venta.[Fecha Documento]like ",
    "insertDocumentDetail":"INSERT INTO [dbo].[DETALLE_DOCUMENTO]([id],[line],[quantity],[netUnitValue],[totalUnitValue],[netAmount],[taxAmount],[totalAmount],[netDiscount],[totalDiscount],[idVariante],[descriptionVariante],[codeVariante],[note],[relatedDetailId],[idDocumento])"
}