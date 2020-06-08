from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    #URLS LOGGIN
    path('', views.InicioSesion, name="InicioSesion"), #1

    path('setLogin', views.setLogin, name="setLogin"), #1
    path('mainHostal', views.mainHostal, name="mainHostal"), #12

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
    path('EditarProveedor/', views.EditarProveedor, name="EditarProveedor"), #27
    path('generarOrdenDePedidos/', views.generarOrdenDePedidos, name="generarOrdenDePedidos"), #30 31 32 33
    path('AdministracionHabitaciones/', views.AdministracionHabitaciones, name="AdministracionHabitaciones"), #37 -43
    path('AdministracionMenu/', views.AdministracionMenu, name="AdministracionMenu"), #44 -46

    #URLS PROVEEDOR

   path('ProveedorOrdenDePedidos/', views.ProveedorOrdenDePedidos, name="ProveedorOrdenDePedidos"), #34 -36

    #Metodos
    path('GuardarNuevoUsuario/', views.GuardarNuevoUsuario, name="GuardarNuevoUsuario"),
    path('GuardarNuevoCliente/', views.GuardarNuevoCliente, name="GuardarNuevoCliente"),
    path('GuardarFormulario/', views.GuardarFormulario, name="GuardarFormulario"),
    path('GuardarNuevoProvedor/', views.GuardarNuevoProvedor, name="GuardarNuevoProvedor"),
    path('ModuloRegistrarHuesped/', views.ModuloRegistrarHuesped, name="ModuloRegistrarHuesped"),
    path('getOrdenCompra/', views.getOrdenCompra, name="getOrdenCompra"),
    #path('EditarCliente/<int:organismo_id>', views.EditarCliente, name="EditarCliente"),
    

]
