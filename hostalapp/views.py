from .models import (HAsistente, HOrganismo, HUsuario, HUsuarioPerfil, HOrdenCompra,
HPersona, HOcHuesped,HRegion,HComuna,HOrdenPedido, HHabitacion , HHabitacionTipo , HHabitacionEstado , HMenu, HPlato, HPersonaDireccion, HUsuario, HPagoForma, HHuespedHabitacion)
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .functions import encode, decode, checkSession, getSecuenciaId, usuarioActual
import json
from django.contrib import messages
from django.db import connection
from django.db.models import Q
import sys
from datetime import date
from datetime import datetime

acceso = {
    2:
        {
            "status":"success",
            "uri":"mainHostal",
        },
    3:
        {
            "status":"success",
            "uri":"AdministracionCliente",
        },
    4:
        {
            "status":"success",
            "uri":"ProveedorOrdenDePedidos",
        },
}


WORDFISH = '1236545dasdas$'
ayudaDb = HAsistente.objects.all()

form = {}
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
        request.session["accesoId"]=''
    except:
        print("No se encontró la sesion")

    ayuda = HAsistente.objects.get(modulo_id=1)

    return render(request, "hostal/InicioSesion.html", {'form' : form })

def setLogin(request):

    dataUser = json.loads(request.POST["data"]);

    try:

        print("User "+dataUser["user"])
        usuario=HUsuario.objects.get(username=dataUser["user"]);
        request.session['accesoId'] = usuario.usuario_id

        print("Perfil "+str(usuario.usuario_perfil_id))

        if usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == 2: # ADMINISTRADOR

            data = {
                "status":"success",
                "uri":"mainHostal",
                }

        elif usuario.contrasena == encode(WORDFISH, dataUser["pass"]) and usuario.usuario_perfil_id == 3: # CLIENTE

            data = {
                "status":"success",
                "uri":"/AdministracionCliente",
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
    region = []
    for r in HRegion.objects.all():
        region.append(r)

    form =  {
        "region" : region
    }
    return render(request, "hostal/Formulario.html", {'form':form, 'nav':'/InicioSesion/'})

def GuardarFormulario(request):


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
        return render(request, "hostal/Formulario.html",{'form':form, 'nav':'/InicioSesion/'})

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
        return render(request, "hostal/Formulario.html",{'form':form, 'nav':'/InicioSesion/'})

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

    return render(request, "hostal/InicioSesion.html",{'form':form, 'nav':'/InicioSesion/'})

def SolicitarServicio(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    emp = request.session["oc_empleados"]

    print(emp)

    form = {
        "emp":emp,
        "menu":HMenu.objects.filter(vigencia=1),
        "habitacion":HHabitacion.objects.filter(habitacion_estado_id=1),
        "pagoForma":HPagoForma.objects.all(),
        "ayuda" : ayuda[9]
    }

    return render(request, 'hostal/SolicitarServicio.html', { "form" : form, 'nav':'/AdministracionCliente/'})

def misDatos(request): # DATOS PERSONALES DEL CLIENTE

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    return render(request, 'hostal/misDatos.html')


def AdministracionCliente(request): # ACCESO DEL CLIENTE A SU BANDEJA DE OC

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    usuario=HUsuario.objects.get(usuario_id=request.session['accesoId'])

    sql="""
                    SELECT
                        oc.orden_compra_id orden_compra_id,
                        TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                        TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                        NVL(o.razon_social, 'S/D') organismo_razon_social,
                        NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                        SUM(h.precio) total,
                        (oc.servicio_fin+1)-oc.servicio_inicio dias,
                        (SELECT COUNT(*) cantida FROM h_oc_huesped WHERE orden_compra_id=oc.orden_compra_id) empleados_cantidad,
                        (SELECT COUNT(*) cantida FROM h_oc_huesped WHERE orden_compra_id=orden_compra_id AND recepcion_flag IS NOT NULL) empleados_arrivos_cantidad
                    FROM
                        h_orden_compra oc

                    LEFT JOIN
                        h_oc_huesped och
                        ON
                            oc.orden_compra_id=och.orden_compra_id

                    LEFT JOIN
                        h_huesped_habitacion hh
                        ON
                            och.oc_huesped_id=hh.oc_huesped_id

                    LEFT JOIN
                        h_habitacion h
                        ON
                            hh.habitacion_id=h.habitacion_id

                    LEFT JOIN
                        h_usuario u
                        ON
                            oc.usuario_id=u.usuario_id
                    LEFT JOIN
                        h_organismo o
                        ON
                            oc.organismo_id=o.organismo_id
                    /*WHERE
                        oc.usuario_id=%s*/

                    GROUP BY
                        oc.orden_compra_id,
                        TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY'),
                        TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY'),
                        NVL(o.razon_social, 'S/D'),
                        NVL(o.nombre_fantasia, 'S/D'),
                        (oc.servicio_fin+1)-oc.servicio_inicio

                """ % usuario.usuario_id

    print ("Query : "+sql)
    oc = HOrdenCompra.objects.raw(sql);

    habitacion = HHabitacion.objects.filter(habitacion_estado_id=1)

    form = {
        "oc" : oc,
        "habitacionOk":habitacion.count(),
    }

    return render(request, 'hostal/AdministracionCliente.html', { "form" : form, "nav":"/" })

def AdministracionOrdenesCompra(request): # ADMINISTRACIÒN DE OC PARA EL ADMINISTRADOR.

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    print(ayuda[2])

    sql="""
            SELECT
                oc.orden_compra_id orden_compra_id,
                TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                NVL(o.razon_social, 'S/D') organismo_razon_social,
                NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                (oc.servicio_fin+1)-oc.servicio_inicio dias,
                NVL(SUM(h.precio), 0) total,
                COUNT(och.oc_huesped_id) empleados_cantidad,
                COUNT(ocha.oc_huesped_id) empleados_arrivos_cantidad
            FROM
                h_orden_compra oc
            LEFT JOIN
                h_usuario u
                ON
                    oc.usuario_id=u.usuario_id
            LEFT JOIN
                h_organismo o
                ON
                    oc.organismo_id=o.organismo_id

            LEFT JOIN h_oc_huesped och
                ON oc.orden_compra_id=och.orden_compra_id

            LEFT JOIN h_oc_huesped ocha
                ON oc.orden_compra_id=ocha.orden_compra_id AND
                ocha.recepcion_flag=1

            LEFT JOIN h_huesped_habitacion hh
                ON och.oc_huesped_id=hh.oc_huesped_id

            LEFT JOIN h_habitacion h
                ON
                    hh.habitacion_id=h.habitacion_id

            GROUP BY

                oc.orden_compra_id,
                TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY'),
                TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY'),
                NVL(o.razon_social, 'S/D'),
                NVL(o.nombre_fantasia, 'S/D'),
                (oc.servicio_fin+1)-oc.servicio_inicio

        """

    print ("Query : "+sql)
    oc = HOrdenCompra.objects.raw(sql);

    habitacion=HHabitacion.objects.filter(habitacion_estado_id=1)

    form = {
        "id" : "login",
        "oc" : oc,
        "ayuda" : ayuda[2],
        "habitacionOk":habitacion.count(),
        }

    return render(request, 'hostal/AdministracionOrdenesCompra.html',{ 'form' : form, "nav":"/mainHostal/"})

def Facturas(request):
    form = {
        "ayuda" : ayuda[2],
        }
    return render(request, 'hostal/Facturas.html',{ 'form' : form, "nav":"/mainHostal/"})

def RegistroHuespedes(request):

    request.session["oc_empleados"]=[]
    emp = []

    menu = []

    form = {
        "emp":emp,
        "menu":HMenu.objects.filter(vigencia=1),
<<<<<<< HEAD
        "habitacion":HHabitacion.objects.filter(vigencia=1),
        "lHabitaciones":HHabitacion.objects.all(),
=======
        "habitacion":HHabitacion.objects.filter(habitacion_estado_id=1),
>>>>>>> dcc267017196616e027632837141e11046ecdae7
        "pagoForma":HPagoForma.objects.all(),
        "organismo":HOrganismo.objects.all(),
        "ayuda" : ayuda[9]
    }

    return render (request, 'hostal/RegistroHuespedes.html', {"form" : form, "nav":"/AdministracionOrdenesCompra/"})

def GuardarHuesped(request):

    habitacion=HHabitacion.objects.get(habitacion_id=request.POST["habitacion"])
    try:
        emp=request.session["oc_empleados"]
    except:
        emp = []

    menu=HMenu.objects.get(menu_id=request.POST["menu"])

    empleado={
        "id":len(emp)+1,
        "rut":request.POST["rut_emp"],
        "nombres":request.POST["nombre_persona"],
        "apellido":request.POST["Ap_paterno"],
        "cargo":request.POST["cargo"],
        "habitacionId":request.POST["habitacion"],
        "habitacionRotulo":habitacion.rotulo,
        "menuId":request.POST["menu"],
        "menuNombre":menu.nombre,
    }

    emp.append(empleado)

    try:
        request.session["oc_empleados"]=emp
    except:
        print("No se puso guardar en sesion")

    print(request.POST["organismoId"])

    form = {
        "emp":emp,
        "menu":HMenu.objects.filter(vigencia=1),
        "pagoForma":HPagoForma.objects.all(),
        "habitacion":HHabitacion.objects.filter(habitacion_estado_id=1),
        "organismoId":int(request.POST["organismoId"]),
        "organismo":HOrganismo.objects.all()
    }

    return render(request, 'hostal/RegistroHuespedes.html', { "form": form, "nav":"/AdministracionOrdenesCompra/" })

def removeOCAdmin(request):

    try:
        emp=request.session["oc_empleados"]
    except:
        emp = []

    menu=HMenu.objects.all()
    habitacion=HHabitacion.objects.all()

    empTmp=[]

    for e in emp:

        if str(e["id"]) == request.POST["unsetEmpleado"]:
            print("Excluyendo "+str(e["id"]) )
        else:
            empTmp.append(e)

    request.session["oc_empleados"]=empTmp

    form = {
        "emp":empTmp,
        "menu":HMenu.objects.filter(vigencia=1),
        "habitacion":HHabitacion.objects.filter(habitacion_estado_id=1),
        "organismo":HOrganismo.objects.all(),
        "organismoId":int(request.POST["organismoId"]),
        "pagoForma":HPagoForma.objects.all()
    }

    return render(request, 'hostal/RegistroHuespedes.html', { "form": form, "nav":"/AdministracionOrdenesCompra/", "nav":"/AdministracionOrdenesCompra/" })

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
            print(cliente)

            form = {
                'cliente':cliente
            }

            return render (request, 'hostal/AdminClientesAgregar.html' , { 'form' : form, "nav" : "/mainHostal/" })

            """proveedorResult = HOrganismo.objects.filter(
                    Q(rut__icontains = rut) | Q(nombre_fantasia__containts = nombre) | Q(razon_social__containts = nombre)
                ).filter(organismo_rut=rut)"""

            #proveedor = { proveedorResult }
        except:
            cliente = { }

    elif rut :

        try:
            cliente = HOrganismo.objects.filter(rut__contains=rut)
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
            cliente = HOrganismo.objects.all().exclude(proveedor_flag=1)
        except:
            cliente = { }

    print(cliente)

    form = {
            "buscar" : { "rut" : rut, "nombre" : nombre },
            'cliente' : cliente,
            "ayuda" : ayuda[8]
        }

    return render (request, 'hostal/AdminClientesAgregar.html' , { 'form' : form, "nav" : "/mainHostal/" })


def CrearNuevoCliente(request):

    region = []
    for r in HRegion.objects.all():
        region.append(r)

    form =  {
        "region" : region,
        "ayuda" : ayuda[8]
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

    return render (request, 'hostal/EditarCliente.html', { "form": form, "nav":"/AdminClientesAgregar/"})
def CrearNuevoProovedor(request):

    region = []
    for r in HRegion.objects.all():
        region.append(r)

    form =  {
        "region" : region,
        "ayuda" : ayuda[5]
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
    return render (request, 'hostal/CrearNuevoUsuario.html', { "form" : form, 'nav' : '/mainHostal/' })

def GuardarNuevoUsuario(request): #Al parecer OK
    now = datetime.now()
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

        return render (request,'hostal/CrearNuevoUsuario.html', {'form':form, 'nav' : '/mainHostal/'} )

    else:
        persona.save()

        print("Persona "+str(persona.persona_id))

        usuario.username=request.POST["username"]
        usuario.contrasena=encode(WORDFISH, request.POST["contrasena"])
        usuario.registro_fecha = datetime.now()
        usuario.vigencia=1

        perfil = HUsuarioPerfil.objects.get(usuario_perfil_id=2)

        usuario.usuario_perfil_id=perfil.usuario_perfil_id


        usuario.save()
        try:
            messages.success(request, 'Usuario ha sido creado exitosamente.')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al crear usuario.')

        return render (request, 'hostal/CrearNuevoUsuario.html',{'nav' : '/mainHostal/'})

def AdminProveedor(request):

    if request.POST.get('buscarRut'):
        rut = request.POST.get('buscarRut')
    else:
        rut=''

    if request.POST.get('buscarNombre'):
        nombre = request.POST.get('buscarNombre')
    else:
        nombre=''

    print(request.POST)
    print(rut)

    if rut.strip()!="" and nombre.strip()!="":
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

    elif rut.strip()!="" :

        print("Buscando por rut "+rut)

        try:
            rutLike="%"+rut.upper().strip()+"%"
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
                    UPPER(RUT) LIKE %s
                """

            proveedor=HOrganismo.objects.raw(sql, [rutLike])
#            proveedor = HOrganismo.objects.filter(rut__constains=rut)
        except:
            print("Nos caímos!!!")
            proveedor = { }

    elif nombre.strip()!="":
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
            "ayuda" : ayuda[5]
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
    return render(request, 'hostal/OrdenDePedidos.html',{'ordenPedido':ordenPedido, "form": form, "nav":"/mainHostal/"})


def mainHostal(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesiòn se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    form= {
        "id" : "menu",
        "ayuda" : ayuda[1]
        }

    return render(request, 'hostal/menu.html', { "form": form })

def removeOCEmpleado(request):

    try:
        emp=request.session["oc_empleados"]
    except:
        emp = []

    menu=HMenu.objects.all()
    habitacion=HHabitacion.objects.all()

    empTmp=[]

    for e in emp:

        if str(e["id"]) == request.POST["unsetEmpleado"]:
            print("Excluyendo "+str(e["id"]) )
        else:
            empTmp.append(e)

    request.session["oc_empleados"]=empTmp

    form = {
        "emp":empTmp,
        "menu":HMenu.objects.filter(vigencia=1),
        "habitacion":HHabitacion.objects.filter(habitacion_estado_id=1),
        "pagoForma":HPagoForma.objects.all(),
    }

    return render(request, 'hostal/SolicitarServicio.html', { "form": form, "nav":"/AdministracionCliente/", "nav":"/AdministracionCliente/" })

def ordenCompraHuespedes(request):

    emp = []

    try:
        if request.session["oc_empleados"]=='':
            emp = []
        else:
            emp=request.session["oc_empleados"]
    except:
        emp = []

    menu=HMenu.objects.get(menu_id=request.POST["menu"])
    habitacion=HHabitacion.objects.get(habitacion_id=request.POST["habitacion"])

    empleado={
        "id":len(emp)+1,
        "rut":request.POST["rut_emp"],
        "nombres":request.POST["nombre_persona"],
        "apellido":request.POST["Ap_paterno"],
        "cargo":request.POST["cargo"],
        "habitacionId":request.POST["habitacion"],
        "habitacionRotulo":habitacion.rotulo,
        "menuId":request.POST["menu"],
        "menuNombre":menu.nombre,
    }

    emp.append(empleado)
    request.session["oc_empleados"]=emp

    form = {
        "emp":emp,
        "menu":HMenu.objects.filter(vigencia=1),
        "habitacion":HHabitacion.objects.filter(habitacion_estado_id=1),
        "pagoForma":HPagoForma.objects.all(),
    }

    return render(request, 'hostal/SolicitarServicio.html', { "form": form, "nav":"/AdministracionCliente/" })

def OrdenCompraEnviar(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    try:

        if request.POST["limpiarOc"]:

            request.session["oc_empleador"]=""
            menu=HMenu.objects.get(menu_id=request.POST["menu"])
            habitacion=HHabitacion.objects.get(habitacion_id=request.POST["habitacion"])

            form = {
                "menu":menu,
                "habitacion":habitacion,
                "pagoForma":HPagoForma.objects.all(),
            }

            return render(request, 'hostal/SolicitarServicio.html', { "form": form, "nav":"/mainHostal" })

    except:

        print ("Limpiar OK NO")
        print ("ENVIO "+request.POST["enviarOc"])

    usuarioId=request.session["accesoId"]
    usuario=HUsuario.objects.get(usuario_id=usuarioId)
    emp=request.session["oc_empleados"]
    now = datetime.now()

    print ("Usuario "+str(usuarioId))

    oc_id=getSecuenciaId("H_ORDEN_COMPRA_ORDEN_COMPRA_ID")
    oc=HOrdenCompra(
        orden_compra_id=oc_id,
        servicio_inicio=datetime.now(),
        servicio_fin=datetime.now(),
        organismo_id=190,
        revision_usuario_id=usuarioId,
        visacion_usuario_id=usuarioId,
        factura_emision_flag=0,
        factura_usuario_id=usuarioId,
        usuario_id=usuarioId,
        registro_fecha=datetime.now(),
        nulo_usuario_id=usuarioId)

    oc.save()

    for e in emp:

        existe=1

        try:
            persona=HPersona.objects.get(rut=e["rut"])
        except:
            existe=0

        if existe==0:
            persona=HPersona(
                persona_id = getSecuenciaId("H_PERSONA_PERSONA_ID_SEQ"),
                rut = e["rut"],
                nombres = e["nombres"],
                paterno = e["apellido"],
                materno = "",
                cargo = e["cargo"]
            )
            persona.save()

        pasajero=HOcHuesped(
            oc_huesped_id = getSecuenciaId("H_OC_HUESPED_OC_HUESPED_ID_SEQ"),
            orden_compra = oc,
            persona = persona,
            recepcion_flag = 0
        )
        pasajero.save()

        habitacion=HHabitacion.objects.get(habitacion_id=e["habitacionId"])

        huespedHabitacion=HHuespedHabitacion(
            huesped_habitacion_id = getSecuenciaId("H_HUESPED_HABITACION_HUESPED_H"),
            habitacion = habitacion,
            oc_huesped = pasajero,
        )
        huespedHabitacion.save()

        # ACTUALIZACIÒN DE ESTADO DE HABITACION
        habitacion.habitacion_estado_id=2; # OCUPADA
        habitacion.save()


    request.session["oc_empleados"]=''

    usuario=HUsuario.objects.get(usuario_id=request.session["accesoId"])

    form = {
        "status":"success",
        "msg":"Se ha generado una nueva orden de compra con ID #"+str(oc_id),
    }

    if usuario.usuario_perfil_id==2:
        return render(request, 'hostal/AdministracionOrdenesCompra.html', { "form": form, "nav":"/mainHostal/" })

    elif usuario.usuario_perfil_id==3:
        return render(request, 'hostal/AdministracionCliente.html', { "form": form, "nav":"/" })


def getOrdenCompra(request):

    try:
        print("TODO "+request.POST["todo"])
        if request.POST["todo"]:
            return redirect(to="AdministracionOrdenesCompra");
    except:
        print("Busqueda filtrada.")

    msg = ""

    if request.POST["ocNumero"] == "" and request.POST["cliente"] == "":

        print("Datos sin valor")
        msg = "Para recuperar órdenes de compra se requiere como mínimo un filtro de búsqueda."
        return render(request, 'hostal/AdministracionOrdenesCompra.html', { "msg" : msg, "status" : "error"})

    try:

        ocFlag=0
        clienteFlag=0

        try:
            ocNumero = request.POST["ocNumero"]
        except:
            ocNumero=''

        try:
            cliente = request.POST["cliente"]
        except:
            cliente=''

        print("Oc "+ocNumero)
        print("Cliente "+cliente)

        if ocNumero and ocNumero!='':

            if cliente and cliente!='':

                print("Buscando por OC & Cliente")
                print("OC "+ocNumero+"  / "+cliente)

                cliente='%'+cliente+'%'

                sql="""
                                SELECT
                                    oc.orden_compra_id orden_compra_id,
                                    TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                                    TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                                    NVL(o.razon_social, 'S/D') organismo_razon_social,
                                    NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                                    (oc.servicio_fin+1)-oc.servicio_inicio dias,
                                    (SELECT COUNT(*) cantidad FROM h_oc_huesped och1 WHERE och1.orden_compra_id=oc.orden_compra_id) empleados_cantidad,
                                    (SELECT COUNT(*) cantidad FROM h_oc_huesped och2 WHERE och2.orden_compra_id=oc.orden_compra_id AND och2.recepcion_flag=1) empleados_arrivos_cantidad
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
                                    oc.orden_compra_id="""+ocNumero+""" AND
                                    (
                                        UPPER(o.nombre_fantasia) LIKE UPPER('"""+cliente+"""') OR
                                        UPPER(o.razon_social) LIKE UPPER('"""+cliente+"""'))
                            """

                print ("Query : "+sql)
                oc = HOrdenCompra.objects.raw(sql);

                print("Buscando aplicada")

            else:

                print("Buscando por OC")
                print("OC "+ocNumero)

                sql="""
                                SELECT
                                    oc.orden_compra_id orden_compra_id,
                                    TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                                    TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                                    NVL(o.razon_social, 'S/D') organismo_razon_social,
                                    NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                                    (oc.servicio_fin+1)-oc.servicio_inicio dias,
                                    (SELECT COUNT(*) cantidad FROM h_oc_huesped och1 WHERE och1.orden_compra_id=oc.orden_compra_id) empleados_cantidad,
                                    (SELECT COUNT(*) cantidad FROM h_oc_huesped och2 WHERE och2.orden_compra_id=oc.orden_compra_id AND och2.recepcion_flag IS NOT NULL) empleados_arrivos_cantidad
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
                                    oc.orden_compra_id="""+ocNumero+"""
                            """

                print ("Query : "+sql)
                oc = HOrdenCompra.objects.raw(sql);

                print("Consulta ejecutara")

        elif cliente and cliente != "":

            print("Buscando por Cliente")
            print("cliente "+cliente )

            cliente=cliente.upper()

            oc = HOrdenCompra.objects.raw("""
                            SELECT
                                oc.orden_compra_id orden_compra_id,
                                TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                                TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                                NVL(o.razon_social, 'S/D') organismo_razon_social,
                                NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                                (oc.servicio_fin+1)-oc.servicio_inicio dias,
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

            print ("Query : "+sql)
            oc = HOrdenCompra.objects.raw(sql);

            print("Query ejecutada")

    except:

        print("Se ha producido una excepción ", sys.exc_info()[0])
        oc = {}
        msg = "El criterio de búsqueda utilizado no ha retornado registros."

    form = {
        "oc" : oc,
        "msg" : msg,
    }

    return render(request, 'hostal/AdministracionOrdenesCompra.html', { "form": form, "msg" : msg, "oc" : oc, "status" : "success"})

def generarOrdenDePedidos(request): #template 30

    form = {
            "ayuda" : ayuda[3]
        }

    return render(request, 'hostal/generarOrdenDePedidos.html', { "form" : form, "nav":"/OrdenDePedidos/"})

############ MODULO HABITACIONES

def AdministracionHabitaciones(request): #template 37 -43

    if checkSession(request)==0:
        form ={
            "msg":"La sesiòn se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    listaHabitaciones = HHabitacion.objects.all()
    estadoHabitacion = HHabitacionEstado.objects.all()
    tipoHabitacion = HHabitacionTipo.objects.all()

    print(listaHabitaciones)
    print(estadoHabitacion)
    form = {
            "listaHabitaciones" : listaHabitaciones,
            "estadoHabitacion" : estadoHabitacion,
            "tipoHabitacion" : tipoHabitacion,
            "ayuda" : ayuda[6]
        }

    return render(request, 'hostal/AdministracionHabitaciones.html', { "form" : form, "nav":"/mainHostal/"} )

def Editarhab(request, habitacion_id):


    request.session["habitacion_id"] = str(habitacion_id)


    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    request.session["habitacion_id"] = str(habitacion_id)

    habitacion = HHabitacion.objects.get(habitacion_id = habitacion_id)
    idHabitacion = habitacion.habitacion_id
    habitacionList = HHabitacionTipo.objects.all()

    print(habitacion)

    for h in habitacionList:
        print(str(h.habitacion_tipo_id)+" "+h.descriptor)


    form = {
    'habitacion' : habitacion,
    'tipo' : habitacionList,
    }

    return render(request, 'hostal/Editarhab.html', {'form':form, "nav":"/AdministracionHabitaciones/"})

def updateHab(request):

    habitacion = HHabitacion.objects.get(habitacion_id = request.session["habitacion_id"]);
    habitacionTipo = HHabitacionTipo.objects.get(habitacion_tipo_id = habitacion.habitacion_tipo_id)


    print(habitacionTipo)

    if  habitacion.habitacion_id != request.POST["idHabitacion"] or habitacion.rotulo!= request.POST ["nombreHabitacion"] or habitacion.precio!= request.POST["precioHabitacion"] or habitacion.camas!= request.POST ["camasHabitacion"] or habitacion.accesorios!= request.POST["accesoriosHabitacion"]:

        habitacion = HHabitacion(
        habitacion_id = request.POST['idHabitacion'],
        rotulo = request.POST["nombreHabitacion"],
        habitacion_tipo = HHabitacionTipo.objects.get(descriptor = request.POST['habitacionTipo']),
        habitacion_estado = HHabitacionEstado.objects.get(habitacion_estado_id = 1),
        camas = request.POST["camasHabitacion"],
        accesorios = request.POST["accesoriosHabitacion"],
        precio = request.POST["precioHabitacion"],
        vigencia = 1

        )
        habitacion.save()



    listaHabitaciones = HHabitacion.objects.all()
    estadoHabitacion = HHabitacionEstado.objects.all()
    tipoHabitacion = HHabitacionTipo.objects.all()
    print(habitacion.habitacion_tipo.descriptor)


    form = {
            'habitacion':habitacion,
            'listaHabitaciones':listaHabitaciones,
            'estadoHabitacion':estadoHabitacion,
            'tipoHabitacion':tipoHabitacion,
            'habitacionTipo':habitacionTipo


        }

    return render(request, 'hostal/AdministracionHabitaciones.html', {'form':form, "nav":"/mainHostal/"})

def GuardarNuevaHabitacion(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    descriptor = request.POST["nombre_tipo_habitacion"]

    if HHabitacionTipo.objects.filter(descriptor = descriptor).count() > 0:

        print("Nombre de Habitacion ya existe")

        messages.error(request, "El nombre de la habitacion ya se encuentra registrado")

        return redirect(to="AdministracionHabitaciones")

    nuevoTipoHabitacion = HHabitacionTipo(
            habitacion_tipo_id=getSecuenciaId("H_HABITACION_TIPO_HABITACION_TIPO_ID_SEQ"),
            descriptor= request.POST["nombre_tipo_habitacion"]
            )
    nuevoTipoHabitacion.save()

    return redirect(to="AdministracionHabitaciones")

def AgregarHabitacion(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

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
    print(request.POST["sel"])

    sel=json.loads(request.POST["sel"])
    estadoId=request.POST["estado"]
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

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    listaMenu = HMenu.objects.all()

    listaPlato = HPlato.objects.all()
    print(listaPlato)

    form = {
            'listaMenu':listaMenu,
            "listaPlato" : listaPlato,
            "ayuda" : ayuda[4] # poner el ìndice de la ayuda para esta pantalla
        }

    return render(request, 'hostal/AdministracionMenu.html', { "form" : form, "nav":"/mainHostal/" })


def GuardarPlato(request):

    if checkSession(request)==0:
            form ={
                "msg":"La sesión se encuentra finalizada."
            }
            return render(request, "hostal/InicioSesion.html", { "form":form } )

    now = datetime.now()

    nombre_plato = request.POST["nombre_plato"]


    if HPlato.objects.filter(nombre = nombre_plato).count() > 0:
            messages.error(request, "El nombre del Plato ya se encuentra registrado.")
            listaPlato= HPlato.objects.all()
            listaMenu=HMenu.objects.all()

            form = {
            "datos" : request.POST,
            'listaMenu':listaMenu,
            'listaPlato':listaPlato,
            "ayuda" : ayuda[4]
            }

            return render(request, 'hostal/AdministracionMenu.html', {'form':form, "nav":"/mainHostal/"})

    plato = HPlato(
        plato_id = getSecuenciaId("H_PLATO_PLATO_ID_SEQ"),
        nombre =request.POST["nombre_plato"] ,
        ingredientes = request.POST["ingredientes"],
        valor = request.POST["valor"],
        registro_fecha = datetime.now(),
        vigencia = 1,)

    plato.save()

    listaPlato= HPlato.objects.all()
    listaMenu = HMenu.objects.all()

    form = {
    'listaMenu':listaMenu,
    'listaPlato':listaPlato,
    "ayuda" : ayuda[4]
    }

    print(listaPlato)
    return render(request, 'hostal/AdministracionMenu.html', {'form':form, "nav":"/mainHostal/"})

def GuardarMenu(request):

    #request.session["menu_id"] = str(menu_id)

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    now = datetime.now()

    nombre_menu = request.POST["nombre_menu"]

    if HMenu.objects.filter(nombre = nombre_menu).count() > 0:
        messages.error(request, "El nombre del Menu ya se encuentra en la lista.")
        listaMenu= HMenu.objects.all()
        listaPlato= HPlato.objects.all()

        form = {
        "datos" : request.POST,
        'listaMenu':listaMenu,
        'listaPlato':listaPlato,
        "ayuda" : ayuda[4]
        }

        return render(request, 'hostal/AdministracionMenu.html', {'form':form, "nav":"/mainHostal/"})


    menu = HMenu(
        menu_id= getSecuenciaId("H_MENU_MENU_ID_SEQ"),
        nombre = request.POST["nombre_menu"],
        registro_fecha = datetime.now(),
        vigencia= 1
    )

    menu.save()


    listaPlato=HPlato.objects.all()
    listaMenu= HMenu.objects.all()

    form = {
    'listaPlato':listaPlato,
    'listaMenu':listaMenu,
    "ayuda" : ayuda[4]
    }

    print(listaMenu)
    return render(request, 'hostal/AdministracionMenu.html', {'form':form, "nav":"/mainHostal/"})

def EditarPlato(request,plato_id):

    request.session["plato_id"] = str(plato_id)

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    request.session["menu_id"] = str(menu_id)

    menu = HMenu.objects.get(menu_id = menu_id)
    idMenu = menu.menu_id
    menuList = HMenu.objects.all()

    print(menu)

"""def updateMenu(request, menu_id):

    menu = HHmenu.objects.get(menu_id=request.session["menu_id"]);

    for m in menuList:
        print(str(m.nombre))

    request.session["plato_id"] = str(plato_id)

    plato = HPlato.objects.get(plato_id = plato_id)
    idPlato = plato.plato_id
    platoList = HPlato.objects.all()

    print(plato)
    form = {
    'plato' : plato,
    'tipo' : platoList,
    }

    return render(request, 'hostal/EditarMenu.html', {'form':form, "nav":"/mainHostal/"})
"""

def updateMenu(request):

    menu = HMenu.objects.get(menu_id=request.session["menu_id"]);

    return render(request, 'hostal/EditarPlato.html', {'form':form, "nav":"/AdministracionMenu/"})


def updatePlato(request):

    plato = HPlato.objects.get(plato_id=request.session["plato_id"]);


    print(plato)

    if  plato.nombre != request.POST["nombre_plato"] :

        plato = HPlato(
        plato_id = getSecuenciaId("H_PLATO_PLATO_ID_SEQ"),
        nombre =request.POST["nombre_plato"] ,
        ingredientes = request.POST["ingredientes"],
        valor = request.POST["valor"],
        registro_fecha = datetime.now(),
        vigencia = 1,)

    plato.save()


    listaPlato= HPlato.objects.all()

    form = {
    'plato':plato,
    'listaPlato':listaPlato,
    "ayuda" : ayuda[4]
    }

    return render(request, 'hostal/EditarPlato.html', {'form':form, "nav":"/AdministracionMenu/"})

def Eliminar_plato(request):

    sel=json.loads(request.POST["sel"])
    data = {}

    if len(sel) > 0:

        for selId in sel:

            print("ID "+str(sel[selId]))
            plato = HPlato.objects.get(plato_id=sel[selId])

            plato.delete()

        data = {

            "status" : "success",
            "msg" : "selección eliminada."
        }

    else:

        data = {
            "status" : "error",
            "msg" : "Se ha producido un error al intentar eliminar el Plato, el identificador recibido es inconsistente."
        }

    return HttpResponse(json.dumps(data))


def ProveedorOrdenDePedidos(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

    form = {
            "ayuda" : ayuda[10]
        }
    return render(request, 'hostal/ProveedorOrdenDePedidos.html', { "form" : form })

def AdministracionProductos(request):

    if checkSession(request)==0:
        form ={
            "msg":"La sesión se encuentra finalizada."
        }
        return render(request, "hostal/InicioSesion.html", { "form":form } )

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

def getClienteRut(request):

    dataUser = json.loads(request.POST["data"]);

    print("Rut "+dataUser["rut"])
    rut=dataUser["rut"]

    try:

        persona=HPersona.objects.get(rut=rut)
        data = {
            "status":"success",
            "nombres":persona.nombres,
            "paterno":persona.paterno,
            "materno":persona.materno,
            "cargo":persona.cargo
        }

    except:
        data = {
            "status":"error",
        }

    return HttpResponse(json.dumps(data))

def showOCDetalle(request, oc_id):

    print(oc_id)

    ocHuesped=HOcHuesped.objects.filter(orden_compra_id=oc_id)
    ordenCompra=HOrdenCompra.objects.get(orden_compra_id=oc_id)

    hh = []
    for h in ocHuesped:
        huespedHabitacion=HHuespedHabitacion.objects.get(oc_huesped_id=h.oc_huesped_id)
        habitacion=HHabitacion.objects.get(habitacion_id=huespedHabitacion.habitacion_id)

        persona=HPersona.objects.get(persona_id=h.persona_id)
        hh.append(
            {
                "hh":huespedHabitacion,
                "oc":h,
                "hab":habitacion,
                "p":persona,
            }
        )

    form = {
        "oc" : ordenCompra,
        "hh" : hh,
        "ayuda" : ayuda[10],
        "horaList":range(0, 24),
        "minutoList":range(0, 59),
    }

    return render(request, 'hostal/oc_admin_detalle.html', { "form" : form, "nat": "/AdministracionOrdenesCompra/" })
