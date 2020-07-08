from .models import (HAsistente, HOrganismo, HUsuario, HUsuarioPerfil, HOrdenCompra,
HPersona, HOcHuesped,HRegion,HComuna,HOrdenPedido, HHabitacion , HHabitacionTipo , HHabitacionEstado , HMenu, HPlato, HPersonaDireccion, HUsuario)
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .functions import encode, decode, checkSession, getSecuenciaId, usuarioActual
import json
from django.contrib import messages
from django.db import connection
from django.db.models import Q
import sys
from datetime import date
from datetime import datetime

WORDFISH = '1236545dasdas$'
ayudaDb = HAsistente.objects.all()

form={}
ayuda = {}
for a in ayudaDb:
    ayuda[a.modulo_id]=a.contenido

def getComuna(request):

    data = json.loads(request.POST["data"]);

    try:

        comuna=HComuna.objects.filter(region_id=data["regionId"]);
        html=''
        for c in comuna:
            html = html + '<option value="'+str(c.comuna_id)+'">'+c.nombre+'</option>'

        if html == '':
            html='<option value="0">-Seleccione Región- (Sin comunas)</option>'

        data = {
            'status':'success',
            'html':html,
        }

    except HComuna.DoesNotExist:

        data = {
            'status':'error',
            'html':'html',
            'msg':'La regiòn no tiene comunas asociadas',
        }

    return HttpResponse(json.dumps(data))

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
    form = {
            "ayuda" : ayuda[9]
        }
    return render(request, 'hostal/SolicitarServicio.html', { "form" : form })

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
        "ayuda" : ayuda[2],
        }

    return render(request, 'hostal/AdministracionOrdenesCompra.html',{ 'form' : form })

def Facturas(request):
    return render(request, 'hostal/Facturas.html')

def RegistroHuespedes(request):
    hpd = HPersona.objects.all()
    print(hpd)
    return render (request, 'hostal/RegistroHuespedes.html', {'hpd':hpd})

def GuardarHuesped(request):


    hpd = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        rut=request.POST["rut_empleado"],
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"],
        cargo = request.POST["cargo"]
    )

    hpd.save()

    hpd = HPersona.objects.all()

    return render (request, 'hostal/RegistroHuespedes.html', {'hpd':hpd})

def AdminClientesAgregar(request):

    rut = request.POST.get('buscarRut')
    nombre = request.POST.get('buscarNombre')

    if rut and nombre:
        try:

            nombreLike="%"+nombre.upper()+"%"
            rutLike="%"+rut.upper()+"%"
            sql = """
                SELECT
                    ORGANISMO_ID,
                    RAZON_SOCIAL,
                    RUT,
                    NOMBRE_FANTASIA,
                    GIRO,
                    DIRECCION,
                    TELEFONO,
                    CUENTA_DATOS,
                    PERSONA_ID,
                    USUARIO_ID,
                    TO_CHAR(REGISTRO_FECHA, 'DD/MM/YYYY') REGISTRO_FECHA,
                    PROVEEDOR_FLAG,
                    COMUNA_ID,
                    VIGENCIA

                FROM h_organismo
                WHERE
                    (UPPER(nombre_fantasia) LIKE %s OR
                    UPPER(nombre_fantasia) LIKE %s) AND
                    RUT LIKE %s"""

            cliente = HOrganismo.objects.raw(sql, [nombreLike, nombreLike,rutLike])

            """proveedorResult = HOrganismo.objects.filter(
                    Q(rut__icontains = rut) | Q(nombre_fantasia__containts = nombre) | Q(razon_social__containts = nombre)
                ).filter(organismo_rut=rut)"""

            #proveedor = { proveedorResult }
        except:
            cliente = { }

    elif rut :
        try:
            clienteResult = HOrganismo.objects.get(rut=rut)
            cliente = { clienteResult }
        except:
            cliente = { }

    elif nombre:
        try:
            nombreLike="%"+nombre.upper()+"%"
            sql = """
                SELECT
                    ORGANISMO_ID,
                    RAZON_SOCIAL,
                    RUT,
                    NOMBRE_FANTASIA,
                    GIRO,
                    DIRECCION,
                    TELEFONO,
                    CUENTA_DATOS,
                    PERSONA_ID,
                    USUARIO_ID,
                    TO_CHAR(REGISTRO_FECHA, 'DD/MM/YYYY') REGISTRO_FECHA,
                    PROVEEDOR_FLAG,
                    COMUNA_ID,
                    VIGENCIA
                FROM
                    h_organismo
                WHERE
                    UPPER(nombre_fantasia) LIKE %s OR
                    UPPER(razon_social) LIKE %s"""
            cliente=HOrganismo.objects.raw(sql, [nombreLike, nombreLike])
        except:
            cliente = { }

    else:
        try:
            cliente = HOrganismo.objects.exclude(proveedor_flag=1)
        except:
            cliente = { }

    print(cliente)

    form = {
            "buscar" : { "rut" : rut, "nombre" : nombre },
            'cliente' : cliente,
            "ayuda" : ayuda[5]
        }

    return render (request, 'hostal/AdminClientesAgregar.html' , { 'form' : form, "nav" : "/mainHostal/" })


def CrearNuevoCliente(request):

    region = []
    for r in HRegion.objects.all():
        region.append(r)

    form =  {
        "region" : region
    }

    return render (request, 'hostal/CrearNuevoCliente.html', {'form':form, 'nav':'/AdminClientesAgregar/'})

def GuardarNuevoCliente(request):
    now = datetime.now()

    username = request.POST["username"]
    rutEmpresa = request.POST["rol_empresa"]

    # VALIDANDO NOMRBE DE USUARIO
    if HUsuario.objects.filter(username = username).count() > 0:

        messages.error(request, "El nombre de usuario utilizado ya se encuentra en uso.")

        region = []
        for r in HRegion.objects.all():
            region.append(r)
        form = {
            "datos" : request.POST,
            "region" : region
        }
        return render(request, "hostal/CrearNuevoCliente.html",{'form':form, 'nav':'/AdminClientesAgregar/'})

    # VALIDANDO RUT DEL ORGANISMO
    if HOrganismo.objects.filter(rut = rutEmpresa).count()>0:

        messages.error(request, "El rol inRol de empresa ya se encuentra registrado.")
        region = []
        for r in HRegion.objects.all():
            region.append(r)
        form = {
            'datos':request.POST,
            "region" : region
        }
        return render(request, "hostal/CrearNuevoCliente.html", {'form':form, 'nav':'/AdminClientesAgregar/'})

    # PERSONA
    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )
    persona.save()

    # DIRECCION
    direccionP = HPersonaDireccion(
        persona_direccion_id = getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
        telefono = request.POST["Ptelefono"],
        email =request.POST["Pemail"],
        persona = persona,
        usuario = usuarioActual(), # 56 - Usuario en sesión
        registro_fecha = datetime.now(),
        registro_hora = (now.hour*100)+now.minute
    )
    direccionP.save()

    # USUARIO
    perfil=HUsuarioPerfil.objects.get(usuario_perfil_id=4)
    usuario = HUsuario(
        usuario_id = getSecuenciaId ("H_USUARIO_USUARIO_ID_SEQ"),
        persona=persona,
        username = request.POST["username"],
        contrasena = encode(WORDFISH, request.POST["contrasena"]),
        registro_fecha = datetime.now(),
        usuario_perfil = perfil,
        vigencia = 1
    )
    usuario.save()

    comuna=HComuna.objects.get(comuna_id=request.POST["comunaId"])

    # ORGANISMO
    organismo = HOrganismo(
        organismo_id = getSecuenciaId ("H_ORGANISMO_ORGANISMO_ID_SEQ"),
        razon_social = request.POST["razon_social"],
        rut = request.POST["rol_empresa"],
        nombre_fantasia = request.POST["nombre_fantasia"],
        giro = "", #request.POST["giro"],
        direccion = request.POST["direccion"],
        telefono = request.POST["telefono"],
        cuenta_datos = request.POST["cuenta"],
        persona = persona,
        usuario = usuarioActual(),
        registro_fecha = datetime.now(),
        comuna = comuna,
        vigencia = 1
    )
    organismo.save()

    form = {
        "msg":"Cliente creado exitosamente.",
    }

    try:
        cliente = HOrganismo.objects.distinct(proveedor_flag =1)
    except:
        cliente = { }

    form = {
            'cliente' : cliente
        }

    return render(request, "hostal/CrearNuevoCliente.html", { 'form':form, 'nav':'/mainHostal/' })

def EditarCliente(request, organismo_id):
    request.session["organismo_id"] = str(organismo_id)

    organismo = HOrganismo.objects.get(organismo_id = organismo_id)

    comunaId=organismo.comuna_id
    comuna = HComuna.objects.get(comuna_id=organismo.comuna_id)
    regionId=comuna.region_id

    regionList = HRegion.objects.all()
    comunaList = HComuna.objects.filter(region_id=regionId)
    persona = HPersona.objects.get(persona_id=organismo.persona_id)

    personaDireccion = HPersonaDireccion.objects.filter(persona_id=persona.persona_id).order_by('-registro_fecha', '-registro_hora')[0]

    for r in regionList:
        print(str(r.region_id)+" "+r.nombre)

    form = {
            'organismo':organismo,
            'persona':persona,
            'personaDireccion':personaDireccion,
            'regiones':regionList,
            'comuna':comunaList,
            'comunaId':comunaId,
            'regionId':regionId,
        }

    return render (request, 'hostal/EditarCliente.html', { "form" : form, "nav" : "/AdminClientesAgregar/" } )

def UpdateCliente (request):

    now = datetime.now()

    organismo=HOrganismo.objects.get(organismo_id=request.session["organismo_id"]);
    persona=HPersona.objects.get(persona_id=organismo.persona_id)
    personaDireccion=HPersonaDireccion.objects.filter(persona_id=persona.persona_id)#.order_by("-registro_fecha")[0]

    if persona.nombres!=request.POST["nombre_persona"] or persona.paterno!=request.POST["Ap_paterno"]:

        persona=HPersona(
            persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
            nombres = request.POST["nombre_persona"],
            paterno = request.POST["Ap_paterno"],
            materno = request.POST["Ap_materno"]
        )
        persona.save()

        organismo.persona_id=persona.persona_id

        personaDireccion=HPersonaDireccion(
            persona_direccion_id = getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
            telefono = request.POST["Ptelefono"],
            email = request.POST["Pemail"],
            persona = persona,
            usuario = usuarioActual(), # 56 - Usuario en sesión
            registro_fecha = datetime.now(),
            registro_hora = (now.hour*100)+now.minute
        )
        personaDireccion.save()

    elif personaDireccion.email!=request.POST["Pemail"] or personaDireccion.telefono!=request.POST["Ptelefono"]:

        personaDireccion=HPersonaDireccion(
            persona_direccion_id = getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
            telefono = request.POST["Ptelefono"],
            email = request.POST["Pemail"],
            persona = persona,
            usuario = usuarioActual(), # 56 - Usuario en sesión
            registro_fecha = datetime.now(),
            registro_hora = (now.hour*100)+now.minute
        )
        personaDireccion.save()

    comuna=HComuna.objects.get(comuna_id=request.POST["comunaId"])
    persona=HPersona.objects.get(persona_id=organismo.persona_id)

    organismo.razon_social = request.POST["razon_social"]
    organismo.rut = request.POST["rol_empresa"]
    organismo.nombre_fantasia = request.POST["nombre_fantasia"]
    organismo.direccion = request.POST["direccion"]
    organismo.telefono = request.POST["telefono"]
    organismo.cuenta_datos = request.POST["cuenta"]
    organismo.persona = persona
    organismo.usuario = usuarioActual()
    organismo.registro_fecha = datetime.now()
    organismo.comuna = comuna

    organismo.save()

    comunaId=organismo.comuna_id
    regionId=comuna.region_id

    regionList = HRegion.objects.all()
    comunaList = HComuna.objects.filter(region_id=regionId)

    form = {
            'organismo':organismo,
            'persona':persona,
            'personaDireccion':personaDireccion,
            'regiones':regionList,
            'comuna':comunaList,
            'comunaId':comunaId,
            'regionId':regionId,
            'msg':"Datos actualizados."
        }

    return render (request, 'hostal/EditarCliente.html', { "form": form, "nav":"/AdminClientesAgregar/"})
def CrearNuevoProovedor(request):

    region = []
    for r in HRegion.objects.all():
        region.append(r)

    form =  {
        "region" : region
    }

    return render (request, 'hostal/CrearNuevoProveedor.html', { "form": form, "nav":"/AdminProveedor/"})

def GuardarNuevoProvedor (request):
    now = datetime.now()

    username = request.POST["username"]
    rutEmpresa = request.POST["rol_empresa"]

    # VALIDANDO NOMRBE DE USUARIO
    if HUsuario.objects.filter(username = username).count() > 0:

        messages.error(request, "El nombre de usuario utilizado ya se encuentra en uso.")

        region = []
        for r in HRegion.objects.all():
            region.append(r)
        form = {
            "datos" : request.POST,
            "region" : region
        }
        return render(request, "hostal/CrearNuevoProveedor.html",{'form':form, 'nav':'/AdminProveedor/'})

    # VALIDANDO RUT DEL ORGANISMO
    if HOrganismo.objects.filter(rut = rutEmpresa).count()>0:

        messages.error(request, "El rol inRol de empresa ya se encuentra registrado.")
        region = []
        for r in HRegion.objects.all():
            region.append(r)
        form = {
            'datos':request.POST,
            "region" : region
        }
        return render(request, "hostal/CrearNuevoProveedor.html", {'form':form, 'nav':'/AdminProveedor/'})

    # PERSONA
    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request.POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )
    persona.save()

    # DIRECCION
    direccionP = HPersonaDireccion(
        persona_direccion_id = getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
        telefono = request.POST["Ptelefono"],
        email =request.POST["Pemail"],
        persona = persona,
        usuario = usuarioActual(), # 56 - Usuario en sesión
        registro_fecha = datetime.now(),
        registro_hora = (now.hour*100)+now.minute
    )
    direccionP.save()

    # USUARIO
    perfil=HUsuarioPerfil.objects.get(usuario_perfil_id=4)
    usuario = HUsuario(
        usuario_id = getSecuenciaId ("H_USUARIO_USUARIO_ID_SEQ"),
        persona=persona,
        username = request.POST["username"],
        contrasena = encode(WORDFISH, request.POST["contrasena"]),
        registro_fecha = datetime.now(),
        usuario_perfil = perfil,
        vigencia = 1
    )
    usuario.save()

    comuna=HComuna.objects.get(comuna_id=request.POST["comunaId"])

    # ORGANISMO
    organismo = HOrganismo(
        organismo_id = getSecuenciaId ("H_ORGANISMO_ORGANISMO_ID_SEQ"),
        razon_social = request.POST["razon_social"],
        rut = request.POST["rol_empresa"],
        nombre_fantasia = request.POST["nombre_fantasia"],
        giro = "", #request.POST["giro"],
        direccion = request.POST["direccion"],
        telefono = request.POST["telefono"],
        cuenta_datos = request.POST["cuenta"],
        persona = persona,
        usuario = usuarioActual(),
        registro_fecha = datetime.now(),
        proveedor_flag = 1,
        comuna = comuna,
        vigencia = 1
    )
    organismo.save()

    form = {
        "msg":"Proveedor creado exitosamente.",
    }

    try:
        proveedor = HOrganismo.objects.filter(proveedor_flag =1)
    except:
        proveedor = { }

    form = {
            'proveedor' : proveedor
        }

    return render(request, "hostal/AdminProveedor.html", { 'form':form, 'nav':'/mainHostal/' })

def CrearNuevoUsuario(request):
    form = {
            "ayuda" : ayuda[7]
        }
    return render (request, 'hostal/CrearNuevoUsuario.html', { "form" : form })

def GuardarNuevoUsuario(request): #Al parecer OK

    usuario = HUsuario()

    persona = HPersona(
        persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
        nombres = request .POST["nombre_persona"],
        paterno = request.POST["Ap_paterno"],
        materno = request.POST["Ap_materno"]
    )

    pDireccion = HPersonaDireccion(
        persona_direccion_id = getSecuenciaId("H_PERSONA_DIRECCION_PERSONA_DI"),
        email = request.POST ["email"]

        )


    usuario.persona_id=persona.persona_id

    usuario.username=request.POST["username"]
    #validacion de que usuario ya existe!
    if HUsuario.objects.filter(username= usuario.username).count() > 0:


        messages.error(request, "Nombre de Usuario "+ usuario.username+" ya existe.")

        print("Usuario ", usuario.username, " ya existe")
        print(persona.nombres+' '+ persona.paterno +' '+persona.materno)

        form = {
        'persona':persona,
        'pDireccion':pDireccion
        }

        return render (request,'hostal/CrearNuevoUsuario.html', {'form':form} )

    else:
        persona.save()

        print("Persona "+str(persona.persona_id))
        usuario.username=request.POST["username"]
        usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
        usuario.vigencia=1

        perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=2)

        usuario.usuario_perfil_id=perfil.usuario_perfil_id


        usuario.save()
        try:
            messages.success(request, 'Usuario ha sido creado exitosamente.')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear usuario.')

        return render (request, 'hostal/CrearNuevoUsuario.html')

def AdminProveedor(request):

    rut = request.POST.get('buscarRut')
    nombre = request.POST.get('buscarNombre')

    if rut and nombre:
        try:

            nombreLike="%"+nombre.upper()+"%"
            rutLike="%"+rut.upper()+"%"
            sql = """
                SELECT
                    ORGANISMO_ID,
                    RAZON_SOCIAL,
                    RUT,
                    NOMBRE_FANTASIA,
                    GIRO,
                    DIRECCION,
                    TELEFONO,
                    CUENTA_DATOS,
                    PERSONA_ID,
                    USUARIO_ID,
                    TO_CHAR(REGISTRO_FECHA, 'DD/MM/YYYY') REGISTRO_FECHA,
                    PROVEEDOR_FLAG,
                    COMUNA_ID,
                    VIGENCIA

                FROM h_organismo
                WHERE
                    (UPPER(nombre_fantasia) LIKE %s OR
                    UPPER(nombre_fantasia) LIKE %s) AND
                    RUT LIKE %s"""

            proveedor = HOrganismo.objects.raw(sql, [nombreLike, nombreLike,rutLike])

            """proveedorResult = HOrganismo.objects.filter(
                    Q(rut__icontains = rut) | Q(nombre_fantasia__containts = nombre) | Q(razon_social__containts = nombre)
                ).filter(organismo_rut=rut)"""

            #proveedor = { proveedorResult }
        except:
            proveedor = { }

    elif rut :
        try:
            proveedorResult = HOrganismo.objects.get(rut=rut)
            proveedor = { proveedorResult }
        except:
            proveedor = { }

    elif nombre:
        try:
            nombreLike="%"+nombre.upper()+"%"
            sql = """
                SELECT
                    ORGANISMO_ID,
                    RAZON_SOCIAL,
                    RUT,
                    NOMBRE_FANTASIA,
                    GIRO,
                    DIRECCION,
                    TELEFONO,
                    CUENTA_DATOS,
                    PERSONA_ID,
                    USUARIO_ID,
                    TO_CHAR(REGISTRO_FECHA, 'DD/MM/YYYY') REGISTRO_FECHA,
                    PROVEEDOR_FLAG,
                    COMUNA_ID,
                    VIGENCIA
                FROM
                    h_organismo
                WHERE
                    UPPER(nombre_fantasia) LIKE %s OR
                    UPPER(razon_social) LIKE %s"""
            proveedor=HOrganismo.objects.raw(sql, [nombreLike, nombreLike])
        except:
            proveedor = { }

    else:
        try:
            proveedor = HOrganismo.objects.filter(proveedor_flag =1)
        except:
            proveedor = { }

    print(proveedor)

    form = {
            "buscar" : { "rut" : rut, "nombre" : nombre },
            'proveedor' : proveedor,
            "ayuda" : ayuda[5]
        }

    return render (request, 'hostal/AdminProveedor.html' , { 'form' : form, "nav" : "/mainHostal/" })



def EditarProveedor(request, organismo_id):

    request.session["organismo_id"] = str(organismo_id)

    organismo = HOrganismo.objects.get(organismo_id = organismo_id)

    comunaId=organismo.comuna_id
    comuna = HComuna.objects.get(comuna_id=organismo.comuna_id)
    regionId=comuna.region_id

    regionList = HRegion.objects.all()
    comunaList = HComuna.objects.filter(region_id=regionId)
    persona = HPersona.objects.get(persona_id=organismo.persona_id)
    personaDireccion = HPersonaDireccion.objects.filter(persona_id=persona.persona_id).order_by('-registro_fecha', '-registro_hora')[0]

    for r in regionList:
        print(str(r.region_id)+" "+r.nombre)

    form = {
            'organismo':organismo,
            'persona':persona,
            'personaDireccion':personaDireccion,
            'regiones':regionList,
            'comuna':comunaList,
            'comunaId':comunaId,
            'regionId':regionId,
        }

    return render (request, 'hostal/EditarProveedor.html', { "form" : form, "nav" : "/AdminProveedor/" } )

def UpdateProveedor (request):

    now = datetime.now()

    organismo=HOrganismo.objects.get(organismo_id=request.session["organismo_id"]);
    persona=HPersona.objects.get(persona_id=organismo.persona_id)
    personaDireccion=HPersonaDireccion.objects.filter(persona_id=persona.persona_id).order_by("-registro_fecha")[0]

    if persona.nombres!=request.POST["nombre_persona"] or persona.paterno!=request.POST["Ap_paterno"]:

        persona=HPersona(
            persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
            nombres = request.POST["nombre_persona"],
            paterno = request.POST["Ap_paterno"],
            materno = request.POST["Ap_materno"]
        )
        persona.save()

        organismo.persona_id=persona.persona_id

        personaDireccion=HPersonaDireccion(
            persona_direccion_id = getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
            telefono = request.POST["Ptelefono"],
            email = request.POST["Pemail"],
            persona = persona,
            usuario = usuarioActual(), # 56 - Usuario en sesión
            registro_fecha = datetime.now(),
            registro_hora = (now.hour*100)+now.minute
        )
        personaDireccion.save()

    elif personaDireccion.email!=request.POST["Pemail"] or personaDireccion.telefono!=request.POST["Ptelefono"]:

        personaDireccion=HPersonaDireccion(
            persona_direccion_id = getSecuenciaId ("H_PERSONA_DIRECCION_PERSONA_DI"),
            telefono = request.POST["Ptelefono"],
            email = request.POST["Pemail"],
            persona = persona,
            usuario = usuarioActual(), # 56 - Usuario en sesión
            registro_fecha = datetime.now(),
            registro_hora = (now.hour*100)+now.minute
        )
        personaDireccion.save()

    comuna=HComuna.objects.get(comuna_id=request.POST["comunaId"])
    persona=HPersona.objects.get(persona_id=organismo.persona_id)

    organismo.razon_social = request.POST["razon_social"]
    organismo.rut = request.POST["rol_empresa"]
    organismo.nombre_fantasia = request.POST["nombre_fantasia"]
    organismo.direccion = request.POST["direccion"]
    organismo.telefono = request.POST["telefono"]
    organismo.cuenta_datos = request.POST["cuenta"]
    organismo.persona = persona
    organismo.usuario = usuarioActual()
    organismo.registro_fecha = datetime.now()
    organismo.comuna = comuna

    organismo.save()

    comunaId=organismo.comuna_id
    regionId=comuna.region_id

    regionList = HRegion.objects.all()
    comunaList = HComuna.objects.filter(region_id=regionId)

    form = {
            'organismo':organismo,
            'persona':persona,
            'personaDireccion':personaDireccion,
            'regiones':regionList,
            'comuna':comunaList,
            'comunaId':comunaId,
            'regionId':regionId,
            'msg':"Datos actualizados."
        }

    return render (request, 'hostal/EditarProveedor.html', { "form": form, "nav":"/AdminProveedor/"})

def OrdenDePedidos(request):
    ordenPedido = HOrdenPedido.objects.all()
    print(ordenPedido)
    form= {  
        "ayuda" : ayuda[3]
        }
    return render(request, 'hostal/OrdenDePedidos.html',{'ordenPedido':ordenPedido, "form": form})


def mainHostal(request):

    form= { 
        "id" : "menu", 
        "ayuda" : ayuda[1]
        }

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
            "ayuda" : ayuda[6]
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
            "ayuda" : ayuda[4] # poner el ìndice de la ayuda para esta pantalla
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

    listaMenu= HMenu.objects.all()
    form = {
    'listaMenu':listaMenu
    }
    print(listaMenu)
    return render(request, 'hostal/AdministracionMenu.html', {'form':form})
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
    form = {
            "ayuda" : ayuda[10]
        }
    return render(request, 'hostal/ProveedorOrdenDePedidos.html', { "form" : form })

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
