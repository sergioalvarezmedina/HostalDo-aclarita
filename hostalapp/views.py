from .models import (HAsistente, HOrganismo, HUsuario, HUsuarioPerfil, HOrdenCompra,
HPersona, HOcHuesped,HRegion,HComuna,HOrdenPedido, HHabitacion , HHabitacionTipo , HHabitacionEstado , HMenu, HPlato,HPersonaDireccion)
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .functions import encode, decode, checkSession, getSecuenciaId
import json
from django.contrib import messages
from django.db import connection
from django.db.models import Q
import sys

WORDFISH = '1236545dasdas$'
ayudaDb = HAsistente.objects.all()

form={}
ayuda = {}
for a in ayudaDb:
    ayuda[a.modulo_id]=a.contenido


def InicioSesion(request):

    try:
        request.sessions["accesoId"]=''
    except:
        print("No se encontró la sesion")

    ayuda = HAsistente.objects.get(modulo_id=1)

    return render(request, "hostal/InicioSesion.html", {'form' : form })

def setLogin(request):

    dataUser = json.loads(request.POST["data"]);

    try:

        print("User "+dataUser["user"])

        usuario=HUsuario.objects.get(username=dataUser["user"]);

        request.session['accesoId']=usuario.usuario_id

        if usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == 2: # ADMINISTRADOR

            data = {
                "status":"success",
                "uri":"mainHostal",
                }

        elif usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == 3: # CLIENTE

            data = {
                "status":"success",
                "uri":"AdministracionCliente",
                }

        elif usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == 4: # PROVEEDOR

            data = {
                "status":"success",
                "uri":"ProveedorOrdenDePedidos",
                }

        else:

            data = {
                "status":"error",
                "msg":"Credenciales incorrectas, reintente nuevamente.",
                "passIni":dataUser["pass"],
                "pass":encode(WORDFISH, dataUser["pass"]),
            }

            request.session['accesoId']=''

    except HUsuario.DoesNotExist:

        data = {
            'status':'error',
            'msg':"Credenciales incorrectas, reintente nuevamente.",
            "passIni":dataUser["pass"],
            "pass":encode(WORDFISH, dataUser["pass"]),
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

def Editarhab(request, habitacion_id):
    habitacion = HHabitacion.objects.get(habitacion_id=habitacion_id)
    return render(request, 'hostal/Editarhab.html')

def AdministracionCliente(request):

    usuario=HUsuario.objects.get(usuario_id=request.session['accesoId'])

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
                        oc.usuario_id=%s
                """ % usuario.usuario_id

    print ("Query : "+sql)
    oc = HOrdenCompra.objects.raw(sql);

    return render(request, 'hostal/AdministracionCliente.html', { "oc" : oc})

def AdministracionOrdenesCompra(request):

    form = {
        "id" : "login",
        "ayuda" : ayuda[3],
        }

    return render(request, 'hostal/AdministracionOrdenesCompra.html',{ 'form' : form })

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

    if HUsuario.objects.filter(username= usuario.username).count() > 0:
        messages.error(request, "Nombre de Usuario ya existe.")
        print("Usuario ", usuario.username, " ya existe")

    else:
        usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
        usuario.vigencia=1
        perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=3)

        usuario.usuario_perfil_id=perfil.usuario_perfil_id

        usuario.save()


    #Direccion Usuario

    direccionP = HPersonaDireccion(
    persona_direccion_id =getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
    telefono = request.POST["Ptelefono"],
    email =request.POST["Pemail"]
        )
    direccionP.persona_id = persona.persona_id
    direccionP.usuario_id = usuario.usuario_id


    cliente.usuario_id = usuario.usuario_id
    cliente.persona_id = usuario.persona_id
    cliente.razon_social = request.POST["razon_social"]

    cliente.rut = request.POST["rol_empresa"]

    if HOrganismo.objects.filter(rut = cliente.rut).count()>0:
        messages.error(request, "Rol de empresa ya se encuentra registrado.")

    cliente.proveedor_flag=1

    cliente.nombre_fantasia = request.POST["nombre_empresa"]

    if HOrganismo.objects.filter(nombre_fantasia=cliente.nombre_fantasia).count()>0:
        messages.error(request, "Nombre de empresa ya se encuentra registrado.")

    else:
        cliente.direccion = request.POST["direccion"]
        cliente.telefono = request.POST["telefono"]

        comuna = HComuna.objects.get(comuna_id=2)
        cliente.comuna_id=comuna.comuna_id
        cliente.vigencia=1

        try:
            direccionP.save()

            cliente.save()
            messages.success(request, 'Registro Exitoso.')
        except Exception as e:
            messages.error(request, 'Ocurrió un error en el Registro.')
    #return HttpResponseRedirect('/GuardarNuevoProvedor/AdminProveedor')
    proveedor=HOrganismo.objects.all()
    form = {
    'proveedor':proveedor}
    return render(request, "hostal/AdminProveedor.html",{'form':form})


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
    #validacion de que usuario ya existe! Aqui estoy trabajando
    if HUsuario.objects.filter(username= usuario.username).count() > 0:
        messages.error(request, "Nombre de Usuario ya existe.")
        print("Usuario ", usuario.username, " ya existe")

        return render (request,'hostal/CrearNuevoUsuario.html')

    else:
        usuario.username=request.POST["username"]
        usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
        usuario.vigencia=1

        perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=2)

        usuario.usuario_perfil_id=perfil.usuario_perfil_id


        usuario.save()

        return render (request, 'hostal/CrearNuevoUsuario.html')

def AdminProveedor(request):

    
    queryset = request.GET.get('buscar')
    if queryset :
        proveedor = HOrganismo.objects.filter(
            Q(rut__icontains = queryset) |
            Q(nombre_fantasia = queryset)
            ).distinct()
        print(proveedor)
        form = {'proveedor':proveedor}

        return render (request, 'hostal/AdminProveedor.html',{'form':form} )
    
    proveedor = HOrganismo.objects.filter(proveedor_flag =1)
    form = {'proveedor':proveedor}

    return render (request, 'hostal/AdminProveedor.html' ,{'form':form})

#def BuscarProveedor(request):

 #   rutProv = request.GET.get('rut', '')
  #  proveedor = HOrganismo.objects.filter(
   #     rut = rutProv ,
    #    proveedor_flag =1,
         
      #  )
    #print(request.GET)

    #return render (request, 'hostal/AdminProveedor.html',{'proveedor':proveedor})


def EditarProveedor(request,organismo_id):

    proveedor = HOrganismo.objects.get(organismo_id = organismo_id)


    direccionP = HPersonaDireccion.objects.get( usuario_id = proveedor.usuario.usuario_id)


    if request.method == 'GET':
        datosOrg ={'rol_empresa':proveedor.rut,'nombre_empresa':proveedor.nombre_fantasia,
        'razon_social':proveedor.razon_social,'direccion':proveedor.direccion,
        'telefono':proveedor.telefono,'nombre_persona':proveedor.persona.nombres,
        'Ap_paterno': proveedor.persona.paterno,'Ap_materno': proveedor.persona.materno,
        'username':proveedor.usuario.username,'Ptelefono': direccionP.telefono,
        'Pemail':direccionP.email}
        #verificar si funka
        return render (request, 'hostal/EditarProveedor.html', datosOrg)

    
    if request.method == 'POST':#para guardar los datos una vez modificados
    
        proveedor.rut = request.POST['rol_empresa']
        proveedor.nombre_fantasia = request.POST ['nombre_empresa']
        proveedor.razon_social = request.POST ['razon_social']
        proveedor.direccion = request.POST ['direccion']
        proveedor.telefono = request.POST ['telefono']
        proveedor.persona.nombres = request.POST['nombre_persona']
        proveedor.persona.paterno = request.POST['Ap_paterno']
        proveedor.persona.materno = request.POST ['Ap_materno']
        proveedor.usuario.username= request.POST['username']
        direccionP.telefono = request.POST ['Ptelefono']
        direccionP.email = request.POST ['Pemail']

        direccionP.save()
        proveedor.save()


        proveedor=HOrganismo.objects.filter(proveedor_flag=1)
        form = {
        'proveedor':proveedor
        }
        return render (request, 'hostal/AdminProveedor.html', {'form':form})



def OrdenDePedidos(request):
    ordenPedido = HOrdenPedido.objects.all()
    print(ordenPedido)
    return render(request, 'hostal/OrdenDePedidos.html',{'ordenPedido':ordenPedido})

def mainHostal(request):

    form={ "id" : "menu", "ayuda" : ayuda[1]}

    return render(request, 'hostal/menu.html', { "form": form })

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

############ MODULO HABITACIONES

def AdministracionHabitaciones(request): #template 37 -43
    listaHabitaciones = HHabitacion.objects.all()
    estadoHabitacion = HHabitacionEstado.objects.all()
    tipoHabitacion = HHabitacionTipo.objects.all()
    print(listaHabitaciones)
    form = {
            "listaHabitaciones" : listaHabitaciones,
            "estadoHabitacion" : estadoHabitacion,
            "tipoHabitacion" : tipoHabitacion,
            "ayuda" : ayuda[3]
        }
    return render(request, 'hostal/AdministracionHabitaciones.html', { "form" : form } )

def Editarhab(request, habitacion_id):
    habitacion = HHabitacion.objects.get(habitacion_id = habitacion_id)

    if request.method == 'GET':
        datosOrg ={'idHabitacion':habitacion.habitacion_id,'nombreHabitacion':habitacion.rotulo,
                   'precioHabitacion':habitacion.precio,'camasHabitacion':habitacion.camas,'accesoriosHabitacion':habitacion.accesorios}

    return render(request, 'hostal/Editarhab.html', datosOrg)


def GuardarNuevaHabitacion(request):

    nuevoTipoHabitacion = HHabitacionTipo(
        habitacion_tipo_id=getSecuenciaId("H_HABITACION_TIPO_HABITACION_TIPO_ID_SEQ"),
        descriptor= request.POST["nombre_tipo_habitacion"]
        )
    nuevoTipoHabitacion.save()

    return redirect(to="AdministracionHabitaciones")

def AgregarHabitacion(request):

    nuevaHabitacion = HHabitacion(
        habitacion_id = request.POST['HabitacionID'],
        rotulo = request.POST["NombreHabitacion"],
        habitacion_tipo = HHabitacionTipo.objects.get(descriptor = request.POST['habitacionTipo']) ,
        habitacion_estado = HHabitacionEstado.objects.get(habitacion_estado_id = 1),
        camas = request.POST["CamasHabitacion"],
        accesorios = request.POST["AccesoriosHabitacion"],
        precio = request.POST["PrecioHabitacion"],
        vigencia = 1

        )
    nuevaHabitacion.save()

    return redirect(to="AdministracionHabitaciones")



def Modificar_EstadoHabitacion(request):

    print(request.POST["estado"])

    sel=json.loads(request.POST["sel"])
    estadoId=json.loads(request.POST["estado"])
    data = {}

    if len(sel) > 0:

        habitacion_estado = HHabitacionEstado.objects.get(habitacion_estado_id=estadoId)

        for selId in sel:

            print("ID "+str(sel[selId]))

            habitacion = HHabitacion.objects.get(habitacion_id=sel[selId])
            habitacion.habitacion_estado=habitacion_estado
            habitacion.save()

        data = {
            "status" : "success",
            "msg" : "selección Modificada."
        }

    else:

        data = {
            "status" : "error",
            "msg" : "Se ha producido un error al intentar modificar la habitación, el identificador recibido es inconsistente."
        }

    return HttpResponse(json.dumps(data))


def Eliminar_habitacion(request):

    sel=json.loads(request.POST["sel"])
    data = {}

    if len(sel) > 0:

        for selId in sel:

            print("ID "+str(sel[selId]))
            habitacion = HHabitacion.objects.get(habitacion_id=sel[selId])
            habitacion.delete()

        data = {

            "status" : "success",
            "msg" : "selección eliminada."
        }

    else:

        data = {
            "status" : "error",
            "msg" : "Se ha producido un error al intentar eliminar la habitación, el identificador recibido es inconsistente."
        }

    return HttpResponse(json.dumps(data))

############ MODULO MENU

def AdministracionMenu(request):
    listaMenu = HMenu.objects.all()
    print(listaMenu)

    form = {
            "listaMenu" : listaMenu,
            "ayuda" : ayuda[3] # poner el ìndice de la ayuda para esta pantalla
        }

    return render(request, 'hostal/AdministracionMenu.html', { "form" : form })

def GuardarMenu(request):

    menu = HMenu(
        menu_id= getSecuenciaId("H_MENU_MENU_ID_SEQ"),
        nombre = request.POST["nombre_menu"],
        vigencia= 1
    )
    print(menu)
    menu.save()

    return render(request, 'hostal/AdministracionMenu.html')
##############################################
def GuardarMenu(request):

    menu = HMenu(
        menu_id= getSecuenciaId("H_MENU_MENU_ID_SEQ"),
        nombre = request.POST["nombre_menu"],
        vigencia= 1
    )
    print(menu)
    menu.save()

    return render(request, 'hostal/AdministracionMenu.html')

#URL PROVEEDOR

def ProveedorOrdenDePedidos(request):
    return render(request, 'hostal/ProveedorOrdenDePedidos.html')

def AdministracionProductos(request):
    return render(request, 'hostal/AdministracionProductos.html')


def getOCEmpleados(request):

    dataIn = json.loads(request.POST["data"]);

    hab = HHabitacion.objects.raw("""
                    SELECT
                        h.habitacion_id habitacion_id,
                        h.rotulo rotulo,
                        ht.descriptor tipo_descriptor
                    FROM
                        h_habitacion h
                    INNER JOIN
                        h_habitacion_tipo ht
                        ON
                            h.habitacion_tipo_id=ht.habitacion_tipo_id

                    INNER JOIN
                        h_habitacion_estado he
                        ON
                            h.habitacion_estado_id=he.habitacion_estado_id

                    WHERE
                        h.vigencia=1
                """
            )

    habitacion=''
    for h in hab:
        habitacion=habitacion+'<option value="'+h.habitacion_id+'">'+h.rotulo+' '+h.habitacion_tipo

    oc=HOcHuesped.objects.filter(oc_huesped_id=dataIn["ocId"]);

    html = ''
    for o in oc:

        persona=HPersona.objects.get(persona_id=o.persona_id)

        cargo="S/D"
        if persona.cargo!="":
            cargo=persona.cargo

        hora=''
        for h in range(0, 24):
            hora=hora+"<option>"+str(h)+"</option>"

        min=''
        for m in range(0, 59):
            min=min+"<option>"+str(m)+"</option>"

        html = html + """
            <tr>
                <td>"""+persona.rut+"""</td>
                <td>"""+persona.nombres+""" """+persona.paterno+""" """+persona.materno+"""  </td>
                <td title=\"Sin dato\">"""+cargo+"""</td>
                <td><input type=\"checkbox\"></td>
                <td>
                    <table width=\"100%\">
                        <tr>
                            <td>
                                <select class="form-control" id="modalOCEmpleadoHHHH">
                                    """+hora+"""
                                </select>
                            </td>
                            <td>
                                <select class="form-control" id="modalOCEmpleadoHHMM">
                                    """+min+"""
                                </select>
                            </td>
                        </tr>
                    </table>
                </td>
                <td>
                    <select id=\"modalOCEmpleadoHabitacion\" class=\"form-control\">
                    """+habitacion+"""
                    </select>
                </td>
            </tr>
            """

    data={
        "status":"success",
        "html":html
    }

    return HttpResponse(json.dumps(data))

def getMenuPlatosSel(request):

    plato=HPlato.objects.all();

    data=[]

    for p in plato:
        data.append(
                {"id":p.plato_id,
                "nombre":p.nombre,
                }
            )

    return HttpResponse(json.dumps(data))

def setMenuPlatosSel(request):

    print(request.POST["data"])

    data = {}

    return HttpResponse(json.dumps(data))
