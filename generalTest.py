from Class.Controller.ClienteController import ClienteController
from Class.Controller.ConsumoController import ConsumoController
from Class.Controller.DescuentoController import DescuentoController
from Class.Controller.DevolucionController import DevolucionController
from Class.Controller.ListaPrecioController import ListaPrecioController
from Class.Controller.ProductController import ProductController
from Class.Controller.ProductTypeController import ProductTypeController
from Class.Controller.RecepcionController import RecepcionController
from Class.Controller.StockController import StockController
from Class.Controller.SucursalController import SucursalController
from Class.Controller.TipoDocumentoController import TipoDocumentoController
from Class.Controller.TipoLibroController import TipoLibroController
from Class.Controller.UsuarioController import UsuarioController
from Class.Controller.VarianteController import VarianteController

from datetime import datetime


inicio = datetime.now()

print("##########################################")
print("Inicio sucursal")
sucursal = SucursalController('sucursal')
sucursal.execute_logic()

print("##########################################")
print("Inicio usuario")
usuario = UsuarioController('usuario')
usuario.execute_logic()

print("##########################################")
print("Inicio Descuento")
descuento = DescuentoController('descuento')
descuento.execute_logic()

print("##########################################")
print("Inicio Tipo Libro")
tlc = TipoLibroController('tipoLibro')
tlc.execute_logic()

print("##########################################")
print("Inicio Tipo Documento")
tdc = TipoDocumentoController('tipoDocumento')
tdc.execute_logic()

print("##########################################")
print("Inicio Tipo Producto")
ptc = ProductTypeController('tipoProducto')
ptc.execute_logic()

print("##########################################")
print("Inicio Producto")
pc = ProductController('producto')
pc.execute_logic()

print("##########################################")
print("Inicio Variante")
vc = VarianteController('variante')
vc.execute_logic()

print("##########################################")
print("Inicio Lista precio")
lpc = ListaPrecioController('listaPrecio')
lpc.execute_logic()

print("##########################################")
print("Inicio Stock")
sc = StockController('stock')
sc.execute_logic()

print("##########################################")
print("Inicio Recepcion")
rc = RecepcionController('recepcion')
rc.execute_logic()

print("##########################################")
print("Inicio Consumo")
cc = ConsumoController('consumo')
cc.executelogic()

print("##########################################")
print("Inicio Cliente")
cc = ClienteController('cliente')
cc.execute_logic()

print("##########################################")
print("Inicio Devolucion")
dc = DevolucionController('devolucion')
dc.execute_logic()

print(datetime.now()-inicio)
