import base64
import cx_Oracle
from django.shortcuts import render
from django.db import connection
from .models import HUsuario, HOrdenCompra
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def checkSession(request):

    print("Chequeando sesiòn")
    print("accesoId "+str(request.session["accesoId"]))

    try:
        if request.session["accesoId"]=='':
            return 0
        else:
            return 1
    except:
        print("No se encontró la sesion")
        return 0

def getSecuenciaId(seq):

    cursor = connection.cursor()
    cursor.execute("SELECT %s.nextval FROM DUAL;" % seq)
    row = cursor.fetchone()

    return row[0]

# simulacion de validaciòn ISSET de php, verifica si variable existe
def isset(variable):

	return variable in locals() or variable in globals()

def usuarioActual():

    usuario=HUsuario.objects.get(usuario_id=56)
    return usuario

def getOrdenCompraCliente(request):

    usuario=HUsuario.objects.get(usuario_id=request.session['accesoId'])

    sql="""
                    SELECT
                        oc.orden_compra_id orden_compra_id,
                        TO_CHAR(oc.servicio_inicio, 'DD/MM/YYYY') servicio_inicio,
                        TO_CHAR(oc.servicio_fin, 'DD/MM/YYYY') servicio_fin,
                        NVL(o.razon_social, 'S/D') organismo_razon_social,
                        NVL(o.nombre_fantasia, 'S/D') organismo_nombre_fantasia,
                        SUM(NVL(h.precio, 0)) total,
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
                    WHERE
                        oc.usuario_id=%s

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

    return oc
