from django.contrib import admin
from django.urls import path
from . import views
from . import urls2
from .views import Eliminar_habitacion, Modificar_EstadoHabitacion

urlpatterns = [

    #URLS LOGGIN
    path('', views.InicioSesion, name="InicioSesion"), #1

    # jquery , post

    path('setLogin', views.setLogin, name="setLogin"), #1
    path('getClienteRut', views.getClienteRut, name="getClienteRut"), #1
    path('getComunaList', views.getComuna, name="getComuna"), #1
    path('mainHostal/', views.mainHostal, name="mainHostal"), #12

    # cliente inserta huesped
    path('ordenCompraHuespedes/', views.ordenCompraHuespedes, name='ordenCompraHuespedes'), # insertar empleado como huesped a una orden  de compra

    path('Formulario/', views.Formulario, name="Formulario"), #3 4 5

    #URLS CLIENTES
    path('AdministracionCliente/', views.AdministracionCliente, name="AdministracionCliente"), #6 7
    path('SolicitarServicio/', views.SolicitarServicio, name="SolicitarServicio"), #8
    path('misDatos/', views.misDatos, name="misDatos"), #9 10 11


    #URLS HOSTAL
    path('AdministracionOrdenesCompra/', views.AdministracionOrdenesCompra, name="AdministracionOrdenesCompra"), #13 14 15
    path('Facturas/', views.Facturas, name="Facturas"), #16 17
    path('RegistroHuespedes/', views.RegistroHuespedes, name="RegistroHuespedes"), #18 19
    path('AdminClientesAgregar/', views.AdminClientesAgregar, name="AdminClientesAgregar"), #20 23
    path('CrearNuevoCliente/', views.CrearNuevoCliente, name="CrearNuevoCliente"),#21
    path('CrearNuevoUsuario/', views.CrearNuevoUsuario, name="CrearNuevoUsuario"), #22
    path('OrdenDePedidos/', views.OrdenDePedidos, name="OrdenDePedidos"), #28
    path('CrearNuevoProovedor/', views.CrearNuevoProovedor, name="CrearNuevoProovedor"), #24 25
    path('AdminProveedor/', views.AdminProveedor, name="AdminProveedor"), #26

    path('generarOrdenDePedidos/', views.generarOrdenDePedidos, name="generarOrdenDePedidos"), #30 31 32 33
    path('AdministracionHabitaciones/', views.AdministracionHabitaciones, name="AdministracionHabitaciones"), #37 -43
    path('AdministracionMenu/', views.AdministracionMenu, name="AdministracionMenu"), #44 -46

    #URLS PROVEEDOR

    path('ProveedorOrdenDePedidos/', views.ProveedorOrdenDePedidos, name="ProveedorOrdenDePedidos"), #34 -36

    path('AdministracionProductos/', views.AdministracionProductos, name="AdministracionProductos"), #47 - 52

    path('Editarhab/<habitacion_id>', views.Editarhab, name="Editarhab"),

    #Metodos
    path('GuardarNuevoUsuario/', views.GuardarNuevoUsuario, name="GuardarNuevoUsuario"),

    path('GuardarFormulario/', views.GuardarFormulario, name="GuardarFormulario"),

    path('GuardarMenu/', views.GuardarMenu, name="GuardarMenu"),
    path('ordenCompraHuespedes/', views.ordenCompraHuespedes, name="ordenCompraHuespedes"),
    path('GuardarNuevaHabitacion/', views.GuardarNuevaHabitacion, name="GuardarNuevaHabitacion"),
    path('AgregarHabitacion/', views.AgregarHabitacion, name="AgregarHabitacion"),
    #PROVEEDOR
    path('EditarProveedor/<int:organismo_id>/', views.EditarProveedor, name="EditarProveedor"),
    path('EditarProveedor/', views.EditarProveedor, name="EditarProveedor"),
    path('UpdateProveedor/', views.UpdateProveedor, name="UpdateProveedor"),
    path('GuardarNuevoProvedor/', views.GuardarNuevoProvedor, name="GuardarNuevoProvedor"),
    #CLIENTE
    path('EditarCliente/<int:organismo_id>/', views.EditarCliente, name="EditarCliente"),
    path('EditarCliente/', views.EditarCliente, name="EditarCliente"),
    path('UpdateCliente/', views.UpdateCliente, name="UpdateCliente"),
    path('GuardarNuevoCliente/', views.GuardarNuevoCliente, name="GuardarNuevoCliente"),

    #path('GuardarHuesped/', views.GuardarHuesped, name="GuardarHuesped"),
    path('getOrdenCompra/', views.getOrdenCompra, name="getOrdenCompra"),

    path('getOCEmpleados', views.getOCEmpleados, name="getOCEmpleados"),

    path('OrdenCompraEnviar/', views.OrdenCompraEnviar, name="OrdenCompraEnviar"),

    # jquery , post
    path('getPlatosSeleccion', views.getMenuPlatosSel, name="getMenuPlatosSel"),
    path('setMinutaPlatos', views.setMenuPlatosSel, name="setMenuPlatosSel"),

    path('unsetHabitacion', views.Eliminar_habitacion, name="Eliminar_habitacion"),
    path('setHabitacioEstado', views.Modificar_EstadoHabitacion, name="Modificar_EstadoHabitacion"),

    path('removeOCEmpleado/', views.removeOCEmpleado, name="removeOCEmpleado"),

]
