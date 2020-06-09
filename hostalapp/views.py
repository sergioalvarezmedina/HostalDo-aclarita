from .models import HAsistente, HOrganismo, HUsuario, HUsuarioPerfil, HOrdenCompra, HPersona, HOcHuesped,HRegion,HComuna,HOrdenPedido
from django.shortcuts import render,HttpResponse
from .functions import encode, decode, checkSession, getSecuenciaId
import json
from django.contrib import messages
from django.db import connection
import sys

WORDFISH = '1236545dasdas$'

def InicioSesion(request):

    try:
        request.sessions["accesoId"]=''
    except:
        print("No se encontró la sesion")

    ayuda = HAsistente.objects.get(modulo_id=1)

    return render(request, "hostal/InicioSesion.html" ,{'ayuda':ayuda})

def setLogin(request):

    dataUser = json.loads(request.POST["data"]);

    try:

        usuario=HUsuario.objects.get(username=dataUser["user"]);

        if usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == "2":

            data = {
                "status":"success",
                "uri":"mainHostal",
                }

        elif usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == "3":

            data = {
                "status":"success",
                "uri":"mainCliente",
                }

        else:

            data = {
                "status":"error",
                "msg":"Credenciales incorrectas, reintente nuevamente.",
                #"pass":encode(WORDFISH, dataUser["pass"]),
            }

        request.session['accesoId']=''

    except HUsuario.DoesNotExist:

        data = {
            'status':'error',
            'msg':"Credenciales incorrectas, reintente nuevamente.",
            #'encode':encode(WORDFISH, dataUser["pass"]),
        }

        request.session['accesoId']=''


    return HttpResponse(json.dumps(data))

def Formulario(request):
    return render(request, "hostal/Formulario.html")

def GuardarFormulario(request):

    cliente = HOrganismo()

    usuario = HUsuario()

    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )

    persona.save()

    print("Persona "+str(persona.persona_id))

    usuario.persona_id=persona.persona_id

    usuario.usuario_id=getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ")
    usuario.username=request.POST["username"]
    usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
    usuario.vigencia=1

    comuna= HComuna()

    perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=3)

    usuario.usuario_perfil_id=perfil.usuario_perfil_id

    usuario.save()

    cliente.usuario_id = usuario.usuario_id
    cliente.persona_id = usuario.persona_id
    cliente.razon_social = request.POST["razon_social"]
    cliente.rut = request.POST["rol_empresa"]
    cliente.nombre_fantasia = request.POST["nombre_empresa"]
    cliente.direccion = request.POST["direccion"]
    cliente.telefono = request.POST["telefono"]

    comuna = HComuna.objects.get(comuna_id=2)
    cliente.comuna_id=comuna.comuna_id
    cliente.vigencia=1


    cliente.save()

    if request.POST["crearCliente"] == 1:
        return render(request, "hostal/Formulario.html",{'insert':1})
    else:
        return render(request, "hostal/AdministracionCliente.html")



def SolicitarServicio(request):
    return render(request, 'hostal/SolicitarServicio.html')

def misDatos(request):
    return render(request, 'hostal/misDatos.html')

def AdministracionCliente(request):

    if checkSession():
        return render(request, 'hostal/AdministracionCliente.html')
    else:

        return render(request, 'hostal/InicioSesion.html', {'msg':'No se ha encontrado ninguna sesión activa'})

def AdministracionOrdenesCompra(request):
    ordenCompra = HOrdenCompra.objects.get()
    return render(request, 'hostal/AdministracionOrdenesCompra.html',{'ordenCompra':ordenCompra})

def Facturas(request):
    return render(request, 'hostal/Facturas.html')

def RegistroHuespedes(request):
    return render (request, 'hostal/RegistroHuespedes.html')

def ModuloRegistrarHuesped(request):

    cliente = HOrganismo()

    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombr_persona"],
        paterno = request.POST["Ap_paterno"],
        cargo = request.POST["cargo"]
    )

    persona.save()

    usuario = HUsuario()
    usuario.usuario_id=getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ")

    usuario.save()

    persona.usuario_id=usuario.usuario_id

    cliente.rut = request.POST["rol_empresa"]
    cliente.nombre_fantasia = request.POST["nombre_empresa"]
    cliente.razon_social="Sin Registro"
    cliente.vigencia=1

    comuna = HComuna.objects.get(comuna_id=2)
    cliente.comuna_id=comuna.comuna_id

    cliente.persona_id = persona.persona_id
    cliente.usuario_id = persona.usuario_id

    cliente.save()

    return render (request, 'hostal/RegistroHuespedes.html')

def AdminClientesAgregar(request):
    listadoClientes = HOrganismo.objects.all()
    print(listadoClientes)
    return render(request, 'hostal/AdminClientesAgregar.html',{'listadoClientes':listadoClientes})

def CrearNuevoCliente(request):
    return render (request, 'hostal/CrearNuevoCliente.html')

def GuardarNuevoCliente(request):

    cliente = HOrganismo()

    usuario = HUsuario()

    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )

    persona.save()

    print("Persona "+str(persona.persona_id))

    usuario.persona_id=persona.persona_id

    usuario.usuario_id=getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ")
    usuario.username=request.POST["username"]
    usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
    usuario.vigencia=1

    perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=3)

    usuario.usuario_perfil_id=perfil.usuario_perfil_id

    usuario.save()

    cliente.usuario_id = usuario.usuario_id
    cliente.persona_id = usuario.persona_id
    cliente.razon_social = request.POST["razon_social"]
    cliente.rut = request.POST["rol_empresa"]
    cliente.nombre_fantasia = request.POST["nombre_empresa"]
    cliente.direccion = request.POST["direccion"]
    cliente.telefono = request.POST["telefono"]

    comuna = HComuna.objects.get(comuna_id=2)
    cliente.comuna_id=comuna.comuna_id
    cliente.vigencia=1


    cliente.save()
    return render(request, "hostal/AdminClientesAgregar.html")

#def EditarCliente(request, organismo_id):

 #   organismo_id= request.GET("organismo_id")
  #  cliente = HOrganismo.objects.filter(id=organismo_id)

   # return render (request, 'hostal/EditarCliente.html')


def CrearNuevoProovedor(request):
    return render (request, 'hostal/CrearNuevoProveedor.html')

def GuardarNuevoProvedor (request):

    cliente = HOrganismo()

    usuario = HUsuario()

    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )

    persona.save()

    print("Persona "+str(persona.persona_id))

    usuario.persona_id=persona.persona_id

    usuario.usuario_id=getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ")
    usuario.username=request.POST["username"]
    usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
    usuario.vigencia=1

    perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=3)

    usuario.usuario_perfil_id=perfil.usuario_perfil_id

    usuario.save()

    cliente.usuario_id = usuario.usuario_id
    cliente.persona_id = usuario.persona_id
    cliente.razon_social = request.POST["razon_social"]
    cliente.rut = request.POST["rol_empresa"]
    cliente.nombre_fantasia = request.POST["nombre_empresa"]
    cliente.direccion = request.POST["direccion"]
    cliente.telefono = request.POST["telefono"]

    comuna = HComuna.objects.get(comuna_id=2)
    cliente.comuna_id=comuna.comuna_id
    cliente.vigencia=1

    try:
        cliente.save()
        messages.success(request, 'Registro Exitoso.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error en el Registro.')
    return render(request, "hostal/Formulario.html")

def CrearNuevoUsuario(request):
    return render (request, 'hostal/CrearNuevoUsuario.html')

def GuardarNuevoUsuario(request):

    usuario = HUsuario()

    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )

    persona.save()

    print("Persona "+str(persona.persona_id))

    usuario.persona_id=persona.persona_id

    usuario.username=request.POST["username"]
    usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
    usuario.vigencia=1

    perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=3)

    usuario.usuario_perfil_id=perfil.usuario_perfil_id


    usuario.save()

    return render (request, 'hostal/CrearNuevoUsuario.html')

def AdminProveedor(request):
    #if 'accesoId' not in request.session['accesoId'] or request.session['accesoId']=="":
        #return render (request, 'hostal/AdminPr    oveedor.html', {'msg':'No se ha encontrado una sesi&oacute;n activa-'})

    proveedor = HOrganismo.objects.filter(proveedor_flag =1)
    return render (request, 'hostal/AdminProveedor.html' ,{'proveedor':proveedor})

def EditarProveedor(request):
    return render (request, 'hostal/EditarProveedor.html')

def OrdenDePedidos(request):
    ordenPedido = HOrdenPedido.objects.all()
    print(ordenPedido)
    return render(request, 'hostal/OrdenDePedidos.html',{'ordenPedido':ordenPedido})

def mainHostal(request):

    return render(request, 'hostal/menu.html')

def getOrdenCompra(request):

    msg = ""

    if request.POST["ocNumero"] == "" and request.POST["cliente"] == "":

        print("Datos sin valor")
        msg = "Para recuperar órdenes de compra se requiere como mínimo un filtro de búsqueda."
        return render(request, 'hostal/AdministracionOrdenesCompra.html', { "msg" : msg, "status" : "error"})

    try:

        ocFlag=0
        clienteFlag=0

        ocNumero = int(request.POST["ocNumero"]) if (request.POST["ocNumero"]!="") else 0
        cliente = request.POST["cliente"] if (request.POST["cliente"]!="") else ''

        print("CLiente "+cliente)

        if "ocNumero" in request.POST and request.POST["ocNumero"]!="":
            ocFlag=1

        if "cliente" in request.POST and request.POST["cliente"]!="":
            clienteFlag=1

        if ocFlag==1 and clienteFlag==1:

            print("Ambos criterios "+request.POST["ocNumero"]+" "+request.POST["ocNumero"])
            oc = HOrdenCompra.objects.raw("SELECT * FROM H_ORDEN_COMPRA WHERE ORDEN_COMPRA_ID=%i", [ocNumero])

        elif ocNumero>0:

            sql="""
                            SELECT
                                oc.orden_compra_id orden_compra_id,
                                TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                                TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                                NVL(o.razon_social, 'S/D') organismo_razon_social,
                                NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                                oc.servicio_fin-oc.servicio_inicio dias,
                                (SELECT COUNT(*) cantida FROM h_oc_huesped WHERE orden_compra_id=oc.orden_compra_id) empleados_cantidad,
                                (SELECT COUNT(*) cantida FROM h_oc_huesped WHERE orden_compra_id=orden_compra_id AND recepcion_flag IS NOT NULL) empleados_arrivos_cantidad
                            FROM
                                h_orden_compra oc
                            INNER JOIN
                                h_usuario u
                                ON
                                    oc.usuario_id=u.usuario_id
                            INNER JOIN
                                h_organismo o
                                ON
                                    oc.organismo_id=o.organismo_id
                            WHERE
                                oc.orden_compra_id=%i
                        """ % ocNumero

            print ("Query : "+sql)
            oc = HOrdenCompra.objects.raw(sql);

        elif cliente != "":

            cliente=cliente.upper()

            oc = HOrdenCompra.objects.raw("""
                            SELECT
                                oc.orden_compra_id orden_compra_id,
                                TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                                TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                                NVL(o.razon_social, 'S/D') organismo_razon_social,
                                NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                                oc.servicio_fin-oc.servicio_inicio dias,
                                (SELECT COUNT(*) cantida FROM h_oc_huesped WHERE orden_compra_id=oc.orden_compra_id) empleados_cantidad,
                                (SELECT COUNT(*) cantida FROM h_oc_huesped WHERE orden_compra_id=orden_compra_id AND recepcion_flag IS NOT NULL) empleados_arrivos_cantidad
                            FROM
                                h_orden_compra oc
                            INNER JOIN
                                h_usuario u
                                ON
                                    oc.usuario_id=u.usuario_id
                            INNER JOIN
                                h_organismo o
                                ON
                                    oc.organismo_id=o.organismo_id
                            WHERE
                                UPPER(o.nombre_fantasia) LIKE UPPER(%s) OR
                                UPPER(o.razon_social) LIKE UPPER(%s)
                        """, [cliente+'%', cliente+'%']
                    )

    except:

        print("Se ha producido una excepción ", sys.exc_info()[0])
        oc = {}
        msg = "El criterio de búsqueda utilizado no ha retornado registros."


    return render(request, 'hostal/AdministracionOrdenesCompra.html', { "msg" : msg, "oc" : oc, "status" : "success"})

def generarOrdenDePedidos(request): #template 30

    return render(request, 'hostal/generarOrdenDePedidos.html')

def AdministracionHabitaciones(request): #template 37 -43
    return render(request, 'hostal/AdministracionHabitaciones.html')

def AdministracionMenu(request):
    return render(request, 'hostal/AdministracionMenu.html')

#URL PROVEEDOR

def ProveedorOrdenDePedidos(request):
    return render(request, 'hostal/ProveedorOrdenDePedidos.html')
