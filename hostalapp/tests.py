from django.test import TestCase

# Create your tests here.
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class usando_unittest(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Chrome(executable_path=r"C:\Users\Hector\HostalDo-aclarita\hostalapp\drivechrome\chromedriver.exe")

	def test_ingreso(self):
		driver = self.driver
		driver.get("http://127.0.0.1:8000/")


######################
#SECCION CLIENTES INTERNOS
######################

#************ MODULO LOGIN CLIENTES INTERNOS

		#VALIDACION INGRESO SISTEMA Y SALIR SISTEMA / LOGIN -> MENU PRINCIPAL

		usuario = driver.find_element_by_id("usuario")
		usuario.send_keys("j.bernal")
		usuario.send_keys(Keys.TAB)
		time.sleep(1)

		clave = driver.find_element_by_id("password")
		clave.send_keys("123123")

		btnentrar = driver.find_element_by_id("entrar")
		btnentrar.click()
		time.sleep(1)

		btncerrar = driver.find_element_by_xpath("/html/body/div[1]/div/a/button")
		btncerrar.click()
		time.sleep(1)

#************ ORDEN DE COMPRA

		#VALIDACION ADMINISTRACION ORDENES DE COMPRA / LOGIN -> MENU PRINCIPAL -> ORDEN DE COMPRA -> 
		usuario = driver.find_element_by_id("usuario")
		usuario.send_keys("j.bernal")
		usuario.send_keys(Keys.TAB)
		time.sleep(1)

		clave = driver.find_element_by_id("password")
		clave.send_keys("123123")

		btnentrar = driver.find_element_by_id("entrar")
		btnentrar.send_keys(Keys.ENTER)
		time.sleep(1)

		btnOrdenCompra = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[1]/button/div")
		btnOrdenCompra.click()
		time.sleep(1)

		AyudaOc = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaOc.click()
		time.sleep(1)

		cerrarAyudaOc = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaOc.click()
		time.sleep(1)

		buscarOc = driver.find_element_by_xpath("//*[@id='ocNumero']")
		buscarOc.send_keys("1")
		buscarOc = driver.find_element_by_xpath("/html/body/div[2]/div/div/form/div/div[2]/div/button")
		buscarOc.click()


		#VALIDACION FACTURA EN AOC /  ORDEN DE COMPRA -> FACTURA  


		buscarFactu = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/table/tbody/tr[1]/th[9]/a/button")
		buscarFactu.click()
		time.sleep(1)

		AyudaFactu = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaFactu.click()
		time.sleep(1)

		cerrarAyudaFactu = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaFactu.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)



		#VALIDACION REGISTRO HUSPED EN AOC /  ORDEN DE COMPRA -> REGISTRAR HUESPED 


		btnRegHuesped = driver.find_element_by_xpath("/html/body/div[4]/a/button/i")
		btnRegHuesped.click()
		time.sleep(1)

		AyudaRegHuesped = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaRegHuesped.click()
		time.sleep(1)

		cerrarAyudaRegHuesped = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaRegHuesped.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)





#************ MODULO ORDEN DE PEDIDOS

		#VALIDACION ORDEN DE PEDIDO / ORDEN DE COMPRA ->ORDEN DE PEDIDO 

		btnOrdePedido = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[2]/button/i")
		btnOrdePedido.click()
		time.sleep(1)

		AyudaOrdePedido = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaOrdePedido.click()
		time.sleep(1)

		cerrarAyudaOrdePedido = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaOrdePedido.click()
		time.sleep(1)

		btnListadoProducto = driver.find_element_by_id("btn ")
		btnListadoProducto.click()
		time.sleep(1)

		btnCerrarListadoProducto = driver.find_element_by_xpath("//*[@id='listarProductos']/div/div/div[3]/button[1]")
		btnCerrarListadoProducto.click()
		time.sleep(1)

		btnGenerarOp = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[4]/a/button/i")
		btnGenerarOp.click()
		time.sleep(1)

		btnBuscarProvee = driver.find_element_by_id("btnProveedor")
		btnBuscarProvee.click()
		time.sleep(1)

		btnCerrarBuscarProvee = driver.find_element_by_xpath("//*[@id='Buscarproveedor']/div/div/div[3]/button[1]")
		btnCerrarBuscarProvee.click()
		time.sleep(1)

		btnBuscarProducto = driver.find_element_by_id("btnProducto")
		btnBuscarProducto.click()
		time.sleep(1)

		btnCerrarBuscarProducto = driver.find_element_by_xpath("//*[@id='Buscarproducto']/div/div/div[3]/button[1]")
		btnCerrarBuscarProducto.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

#************ MODULO ADM MENU

		btnAdmMenu = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[3]/button/i")
		btnAdmMenu.click()
		time.sleep(1)

		AyudaAdmMenu = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaAdmMenu.click()
		time.sleep(1)

		cerrarAyudaAdmMenu = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaAdmMenu.click()
		time.sleep(1)

		btnNuevoMenu = driver.find_element_by_id("btnNuevoMenu")
		btnNuevoMenu.click()
		time.sleep(1)

		btnCerrarNuevoMenu = driver.find_element_by_xpath("//*[@id='NuevoMenu']/div/div/form/div[2]/button[1]")
		btnCerrarNuevoMenu.click()
		time.sleep(1)

		btnAgregarMinuta = driver.find_element_by_id("btnAgregarMinuta")
		btnAgregarMinuta.click()
		time.sleep(1)

		btnCerrarAgregarMinuta = driver.find_element_by_xpath("//*[@id='NuevaMinutaCerrar']")
		btnCerrarAgregarMinuta.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

#************ MODULO PROVEEDORES

		btnProveedores = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[4]/button/i")
		btnProveedores.click()
		time.sleep(1)

		AyudaProveedores = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaProveedores.click()
		time.sleep(1)

		cerrarAyudaProveedores = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaProveedores.click()
		time.sleep(1)

		btnEditarProveedores = driver.find_element_by_xpath("//*[@id='btnEditarProveedor']")
		btnEditarProveedores.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

		btnNuevoProveedor = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div[2]/div[2]/a/button/i")
		btnNuevoProveedor.click()
		time.sleep(1)

		AyudaNuevoProveedores = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		AyudaNuevoProveedores.click()
		time.sleep(1)

		cerrarAyudaProveedores = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyudaProveedores.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

#************ MODULO HABITACIONES

		btnHabitaciones = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[5]/div[1]/button/i")
		btnHabitaciones.click()
		time.sleep(1)

		Ayuda = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		Ayuda.click()
		time.sleep(1)

		cerrarAyuda = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyuda.click()
		time.sleep(1)

		btnEditarHab = driver.find_element_by_xpath("//*[@id='btnEditarHab']")
		btnEditarHab.click()
		time.sleep(1)

		btnCerrarEditarHab = driver.find_element_by_xpath("//*[@id='editar']/div/div/div[3]/button[1]")
		btnCerrarEditarHab.click()
		time.sleep(1)

		btnNuevTipoHab = driver.find_element_by_xpath("//*[@id='btnNuevTipoHab']")
		btnNuevTipoHab.click()
		time.sleep(1)

		btnCerrarNuevTipoHab = driver.find_element_by_xpath("//*[@id='TipoHabitacion']/div/div/div[3]/button[1]")
		btnCerrarNuevTipoHab.click()
		time.sleep(1)

		btnAgregarHab = driver.find_element_by_xpath("//*[@id='btnAgregarHab']")
		btnAgregarHab.click()
		time.sleep(1)

		btnCerrarAgregarHab = driver.find_element_by_xpath("//*[@id='Agregar']/div/div/div[3]/button[1]")
		btnCerrarAgregarHab.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

#************ MODULO USUARIO

		btnUsuario = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[5]/div[2]/button/i")
		btnUsuario.click()
		time.sleep(1)

		Ayuda = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		Ayuda.click()
		time.sleep(1)

		cerrarAyuda = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyuda.click()
		time.sleep(1)

		btnBack = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/a")
		btnBack.click()
		time.sleep(1)

#************ MODULO CLIENTES

		btnClientes = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div/div[5]/div[3]/button/i")
		btnClientes.click()
		time.sleep(1)

		Ayuda = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		Ayuda.click()
		time.sleep(1)

		cerrarAyuda = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyuda.click()
		time.sleep(1)

		btncerrar = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/a/button")
		btncerrar.click()
		time.sleep(1)


######################
#SECCION CLIENTES EXTERNOS
######################

#************ MODULO LOGIN CLIENTES EXTERNOS


		usuario = driver.find_element_by_id("usuario")
		usuario.send_keys("he.corvalan")
		usuario.send_keys(Keys.TAB)
		time.sleep(1)

		clave = driver.find_element_by_id("password")
		clave.send_keys("123")

		btnentrar = driver.find_element_by_id("entrar")
		btnentrar.click()
		time.sleep(1)


#************ MODULO ADMINISTRACION CLIENTES


		Ayuda = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		Ayuda.click()
		time.sleep(1)

		cerrarAyuda = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyuda.click()
		time.sleep(1)

		#btnCantidadEmpleados = driver.find_element_by_xpath("//*[@id='btnCantidadEmpleados']")
		#btnCantidadEmpleados.click()
		#time.sleep(3)
		#btnCantidadEmpleados.send_keys(Keys.ESCAPE)

		#btnMisDatos = driver.find_element_by_xpath("/html/body/div[4]/a[2]")
		#btnMisDatos.click()
		#time.sleep(1)
		#btnMisDatos.send_keys(Keys.ESCAPE)

		btnSolicitarServicio = driver.find_element_by_xpath("/html/body/div[4]/a[1]")
		btnSolicitarServicio.click()
		time.sleep(1)

		Ayuda = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		Ayuda.click()
		time.sleep(1)

		cerrarAyuda = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyuda.click()
		time.sleep(1)

		btncerrar = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/a/button")
		btncerrar.click()
		time.sleep(1)


######################
#SECCION CLIENTES PROVEEDORES
######################

#************ MODULO LOGIN CLIENTES EXTERNOS


		usuario = driver.find_element_by_id("usuario")
		usuario.send_keys("dark1")
		usuario.send_keys(Keys.TAB)
		time.sleep(1)

		clave = driver.find_element_by_id("password")
		clave.send_keys("dark1")

		btnentrar = driver.find_element_by_id("entrar")
		btnentrar.click()
		time.sleep(1)

		Ayuda = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/button/i")
		Ayuda.click()
		time.sleep(1)

		cerrarAyuda = driver.find_element_by_xpath("//*[@id='modalAyuda']/div[1]/div/div[3]/button")
		cerrarAyuda.click()
		time.sleep(1)

		btnVerProductos = driver.find_element_by_xpath("//*[@id='btnbtnVerProductos']")
		btnVerProductos.click()
		time.sleep(1)

		btnCerrarVerProductos = driver.find_element_by_xpath("//*[@id='listarProductos']/div/div/div[3]/button")
		btnCerrarVerProductos.click()
		time.sleep(1)

		btncerrar = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/a/button")
		btncerrar.click()
		time.sleep(1)






	#def tearDown(self):
	#	self.driver.close()
if __name__ == '__main__':
	unittest.main()