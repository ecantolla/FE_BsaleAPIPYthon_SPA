from Class.Controller.SusucrsalController import SucursalController
from Class.Controller.UsuarioController import UsuarioController
from Class.Controller.DescuentoController import DescuentoController
from Class.Controller.TipoLibroController import TipoLibroController
from Class.Controller.TipoDocumentoController import TipoDocumentoController
from Class.Controller.ProductTypeController import ProductTypeController
from Class.Controller.ProductController import ProductController
from Class.Controller.VarianteController import VarianteController
from Class.Controller.ListaPrecioController import ListaPrecioController
from Class.Controller.StockController import StockController
from Class.Controller.RecepcionController import RecepcionController
from Class.Controller.ConsumoController import ConsumoController
from Class.Controller.ClienteController import ClienteController
from Class.Controller.DevolucionController import DevolucionController
from Class.ConnectionHandler import ConnectionHandler

from datetime import datetime

inicio=datetime.now()
print("##########################################")
print("Inicio sucursal")
sucursal=SucursalController()
sucursal.executelogic()
print("##########################################")
print("Inicio usuario")
usuario=UsuarioController()
usuario.executelogic()
print("##########################################")
print("Inicio Descuento")
descuento=DescuentoController()
descuento.executelogic()
print("##########################################")
print("Inicio Tipo Libro")
tp=TipoLibroController()
tp.executelogic()
print("##########################################")
print("Inicio Tipo Documento")
tc=TipoDocumentoController()
tc.executelogic()
print("##########################################")
print("Inicio Tipo Producto")
tp=ProductTypeController()
tp.executelogic()
print("##########################################")
print("Inicio Producto")
tp=ProductController()
tp.executelogic()
print("##########################################")
print("Inicio Variante")
tp=VarianteController()
tp.executelogic()
print("##########################################")
print("Inicio Lista precio")
tp=ListaPrecioController()
tp.executelogic()

print("##########################################")
print("Inicio Stock")
tp=StockController()
tp.executelogic()

print("##########################################")
print("Inicio Recepcion")
tp=RecepcionController()
tp.executelogic()

print("##########################################")
print("Inicio Consumo")
tp=ConsumoController()
tp.executelogic()

print("##########################################")
print("Inicio Cliente")
tp=ClienteController()
tp.executelogic()

print("##########################################")
print("Inicio Devolucion")
tp=DevolucionController()
tp.executelogic()

print(datetime.now()-inicio)