import datetime

from django.db.models import Sum


def Attr(cls):
    model= cls.__name__
    return cls.__doc__.replace(model,"").replace("(","").replace(")","").replace(" ","").split(",")

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
    #print("horas",horas,"minutos",minutos)
    return "%s:%s:00"%(str.zfill(str(int(horas)),2),str.zfill(str(int(minutos)),2))

def estadistica_mes(lista,anio=datetime.datetime.now().year):
    meses=[]
    for x in range(1,13):
        mes=lista.filter(fecha__month=x ,fecha__year=anio)
        meses.append(int(sumatoriaHoras(mes).split(":")[0]))
        print("estadistica horas:",x,sumatoriaHoras(mes).split(":")[0])
    print(meses)
    return meses

def estadistica_dias(lista,anio=datetime.datetime.now().year):
    dias=[]
    for x in range(1,13):
        dia=lista.filter(fecha__month=x ,fecha__year=anio).aggregate(Sum('dias'))
        if dia["dias__sum"]!=None:
            dias.append(float(dia["dias__sum"]))
        else:
            dias.append(0)

    print(dias)
    return dias

