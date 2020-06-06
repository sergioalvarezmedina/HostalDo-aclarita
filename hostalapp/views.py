from .models import HAsistente, HOrganismo, HUsuario, HUsuarioPerfil, HOrdenCompra, HPersona, HOcHuesped,HRegion,HComuna
from django.shortcuts import render,HttpResponse
from .functions import encode, decode, checkSession, getSecuenciaId
import json
from django.contrib import messages

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

        if usuario.contrasena == encode(WORDFISH, dataUser["pass"]):

            data = {
                'status':'success',
                'uri':'mainHostal',
                #'encode':encode(WORDFISH, dataUser["pass"]),
                #'pass':usuario.contrasena,
            }

            request.session['accesoId']=dataUser["user"]

        else:

            data = {
                'status':'error',
                'msg':"Credenciales incorrectas, reintente nuevamente.",
                #'encode':encode(WORDFISH, dataUser["pass"]),
                #'pass':usuario.contrasena,
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



def Iconos(request):
    ayuda = HAsistente.objects.get(modulo_id=2)
    return render(request, "hostal/Iconos.html", {'ayuda':ayuda})

def SolicitarServicio(request):
    return render(request, 'hostal/SolicitarServicio.html')

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
        #return render (request, 'hostal/AdminProveedor.html', {'msg':'No se ha encontrado una sesi&oacute;n activa-'})

    proveedor = HOrganismo.objects.get(proveedor_flag=1)
    return render (request, 'hostal/AdminProveedor.html', {'proveedor':proveedor})

def EditarProovedor(request):
    return render (request, 'hostal/EditarProovedor.html')

def OrdenDePedidos(request):
    #ordenPedido = HOrdenPedido.objects.get(orden_pedido_id=1)
    return render (request, 'hostal/OrdenDePedidos.html')#,{'ordenPedido':ordenPedido})

def mainHostal(request):

    return render(request, 'hostal/menu.html')

def getOrdenCompra(request):

    return render(request, 'hostal/AdministracionOrdenesCompra.html')
