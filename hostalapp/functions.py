import base64
import cx_Oracle
from django.shortcuts import render
from django.db import connection
from .models import HUsuario

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
