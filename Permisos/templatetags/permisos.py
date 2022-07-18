import datetime

from django import template

from Permisos.models import SolicitudPermiso

register = template.Library()

@register.simple_tag
def sumatoriaHoras(id_usuario,anio=datetime.datetime.now().year):
    lista=SolicitudPermiso.objects.filter(persona__user_id=id_usuario,fecha__year=anio)
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
    return "%s:%s:00"%(str.zfill(str(int(horas)),2),str.zfill(str(int(minutos)),2))

@register.simple_tag
def cantidadRegistros(id_usuario,anio=datetime.datetime.now().year):
    return SolicitudPermiso.objects.filter(persona__user_id=id_usuario,fecha__year=anio).count()

@register.simple_tag
def cantidadDias(id_usuario,anio=datetime.datetime.now().year):
    horas=sumatoriaHoras(id_usuario,anio)
    fraccionhora = int(horas.split(":")[1]) / 60
    total = (fraccionhora + int(horas.split(":")[0])) / 8
    print("total de dias es:", total)
    return total
