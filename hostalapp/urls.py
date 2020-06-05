from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    #URLS CLIENTES
    path('', views.InicioSesion, name="InicioSesion"), #1

    path('setLogin', views.setLogin, name="setLogin"), #1
    path('mainHostal', views.mainHostal, name="mainHostal"), #1

    path('Formulario/', views.Formulario, name="Formulario"), #3 4 5
    path('AdministracionCliente/', views.AdministracionCliente, name="AdministracionCliente"), #6 7
    path('SolicitarServicio/', views.SolicitarServicio, name="SolicitarServicio"), #8
    #9 10 11 falta (misdatos)

    #URLS HOSTAL
    path('Iconos/', views.Iconos, name="Iconos"),   #12
    path('AdministracionOrdenesCompra/', views.AdministracionOrdenesCompra, name="AdministracionOrdenesCompra"), #13 14 15
    path('Facturas/', views.Facturas, name="Facturas"), #16 17
    path('RegistroHuespedes/', views.RegistroHuespedes, name="RegistroHuespedes"), #18 19
    path('AdminClientesAgregar/', views.AdminClientesAgregar, name="AdminClientesAgregar"), #20 23
    path('CrearNuevoCliente/', views.CrearNuevoCliente, name="CrearNuevoCliente"),#21
    path('CrearNuevoUsuario/', views.CrearNuevoUsuario, name="CrearNuevoUsuario"), #22
    path('OrdenDePedidos/', views.OrdenDePedidos, name="OrdenDePedidos"), #28
    path('CrearNuevoProovedor/', views.CrearNuevoProovedor, name="CrearNuevoProovedor"), #24 25
    path('AdminProveedor/', views.AdminProveedor, name="AdminProveedor"), #26
    path('EditarProovedor/', views.EditarProovedor, name="EditarProovedor"), #27

    #Metodos
    path('GuardarNuevoUsuario/', views.GuardarNuevoUsuario, name="GuardarNuevoUsuario"),
    path('GuardarNuevoCliente/', views.GuardarNuevoCliente, name="GuardarNuevoCliente"),
    path('GuardarFormulario/', views.GuardarFormulario, name="GuardarFormulario"),
    path('GuardarNuevoProvedor/', views.GuardarNuevoProvedor, name="GuardarNuevoProvedor"),
    path('ModuloRegistrarHuesped/', views.ModuloRegistrarHuesped, name="ModuloRegistrarHuesped"),
    

]
