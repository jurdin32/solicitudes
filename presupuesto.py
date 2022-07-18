import os
from solicitudes.settings import BASE_DIR
paths=[
    os.path.join(BASE_DIR,'Permisos'),
    os.path.join(BASE_DIR,'Suministros'),
]
total= 0
def numLineasFichero(data):
    archivo=str(data)
    fichero = open(archivo, 'r')
    fichero.readline()
    fichero.seek(0)
    c=len(fichero.readlines())
    fichero.close()
    return c

for path in paths:
    contador =0
    lectura=len(path.split('.'))
    if lectura==1:
        for fichero in os.listdir(path):
            try:
                for f in os.listdir(path+"/"+fichero):
                    if f.endswith('py') or f.endswith('html'):
                        data=(os.path.join(path, fichero+"/"+f))
                        contador+=numLineasFichero(data)
            except:
                data=(os.path.join(path, fichero))
                contador+=numLineasFichero(data)
    else:
        contador = numLineasFichero(path)
    total +=contador
    print('Total de Lineas:',str.zfill(str(contador),4),'en la ruta:',path)

lineas_dia=30
valor_linea=.25

print('Total de lineas:',total)

tiempo_estimado=round((total/lineas_dia),2)
print('Tiempo estimado, en horas:',tiempo_estimado)

dias=round(((total/lineas_dia)/24),2)
print('Tiempo estimado, en dias de 24 horas:',dias)


dias_8=round(((total/lineas_dia)/8),2)
print('Tiempo estimado, en dias de 8 horas:',dias_8)

print('Valor estimado, por dia de 8 horas:',round(((total*valor_linea)/dias_8),2))

print('Valor estimado, por dia:',round(((total*valor_linea)/dias),2))

print('Presupuesto:',round((total*valor_linea),2))