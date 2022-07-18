import datetime
from os import path

import qrcode
from django.db.models import Sum
from io import  BytesIO
import os

from django.conf import settings
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse

from solicitudes.settings import BASE_DIR


def Attr(cls):
    model= cls.__name__
    return cls.__doc__.replace(model,"").replace("(","").replace(")","").replace(" ","").split(",")

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("utf8")),result,link_callback=fetch_resources)
    return HttpResponse(result.getvalue(),content_type="application/pdf")



def convertir_horas(hora,minuto):
    fraccionhora=minuto/60
    total=(fraccionhora+hora)/8
    print("total de dias es:",total)
    return total

def sumatoriaHoras(lista):
    horas=0
    minutos=0
    for x in lista:
        dato=x.cantidad_horas.split(":")
        print(dato)
        minutos+=float(dato[1])
        horas+=float(dato[0])
    if minutos>=60:
        tt=minutos/60
        horas+=int(tt)
        mod=minutos%60
        minutos=mod
    if horas==0 and minutos==0:
        return "00:00:00"
    print("Son: %s:%s:00"%(str.zfill(str(int(horas)),2),str.zfill(str(int(minutos)),2)))
    return "%s:%s:00"%(str.zfill(str(int(horas)),2),str.zfill(str(int(minutos)),2))

def estadistica_mes(lista,anio=datetime.datetime.now().year):
    meses=[]
    for x in range(1,13):
        mes=lista.filter(fecha_salida__month=x ,fecha_salida__year=anio)
        meses.append(int(sumatoriaHoras(mes).split(":")[0]))
    return meses

def estadistica_dias(lista,anio=datetime.datetime.now().year):
    dias=[]
    for x in range(1,13):
        dia=lista.filter(fecha_salida__month=x ,fecha_salida__year=anio).aggregate(Sum('dias'))
        if dia["dias__sum"]!=None:
            dias.append(float(dia["dias__sum"]))
        else:
            dias.append(0)
    print(dias)
    return dias

def generarCodigoQR(cedula,nombres, apellidos,cargo,unidad):
    ruta=path.join(BASE_DIR,'media/qr/%s.png'%cedula)
    img = qrcode.make(
        """ 
        CEDULA: %s
        NOMBRE: %s
        CARGO:  %s
        UNIDAD: %s
        """%(cedula,nombres+" "+apellidos,cargo,unidad)
    )
    f = open(ruta, "wb")
    img.save(f)
    f.close()

def generarCodigoQRJefe(nombres,unidad):
    ruta=path.join(BASE_DIR,'media/qr/%s.png'%nombres)
    img = qrcode.make(
        """
         NOMBRE: %s
         UNIDAD: %s
        """%(nombres,unidad)
    )
    f = open(ruta, "wb")
    img.save(f)
    f.close()
