import datetime

from django.contrib.auth.models import User
from django.db import models

from solicitudes.snniper import convertir_horas

class Anios(models.Model):
    anio=models.IntegerField(default=datetime.datetime.now().year)

    def __str__(self):
        return str(self.anio)

class Configuracion(models.Model):
    numero_solicitud=models.IntegerField(default=1)
    numero_materiales=models.IntegerField(default=1)
    nombre_director_th=models.CharField(max_length=60, default='Soc.Ramiro Michelena Ch.')

    class Meta:
        verbose_name_plural='1. Configuración'


class Funcionarios(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cargo=models.CharField(max_length=100)
    direccion=models.CharField(max_length=100)
    jefe_inmediato=models.CharField(max_length=100)
    director_th=models.CharField(max_length=100, default="Soc. Ramiro Michelena")
    estado=models.BooleanField(default=True)

    def __str__(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)

    class Meta:
        verbose_name_plural='2. Funcionarios'

class SolicitudPermiso(models.Model):
    numero_solicitud=models.CharField(max_length=10,null=True,blank=True)
    fecha=models.DateField(auto_now_add=True)
    persona=models.ForeignKey(Funcionarios, on_delete=models.CASCADE)
    fecha_salida=models.DateField(null=True,blank=True)
    fecha_entrada=models.DateField(null=True,blank=True)
    hora_salida=models.TimeField(null=True,blank=True)
    hora_entrada=models.TimeField(null=True,blank=True)
    cantidad_horas = models.CharField(max_length=100,null=True,blank=True)
    dias=models.DecimalField(max_digits=9, decimal_places=2, default=0)
    particular=models.BooleanField(default=False)
    calamidad_domestica=models.BooleanField(default=False)
    enfermedad=models.BooleanField(default=False)
    otros=models.BooleanField(default=False)
    otro=models.CharField(max_length=100, null=True,blank=True)
    observaciones=models.TextField()

    class Meta:
        verbose_name_plural='3. Solicitudes de Permisos'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        contador=SolicitudPermiso.objects.count()+Configuracion.objects.first().numero_solicitud
        if not self.numero_solicitud:
            self.numero_solicitud=str.zfill(str(contador),10)

        if self.hora_salida!=None and self.hora_entrada!=None:
            formato = "%H:%M:%S"
            d1 = datetime.datetime.strptime(str(self.hora_entrada),formato)
            d2 = datetime.datetime.strptime(str(self.hora_salida),formato)
            self.cantidad_horas=str(d1-d2)
            dato=self.cantidad_horas.split(":")
            convertir_horas(int(dato[0]),int(dato[1]))
            self.dias=convertir_horas(int(dato[0]),int(dato[1]))

        if self.fecha_salida!=None and self.fecha_entrada!=None:
            formato= '%Y-%m-%d'
            f1=datetime.datetime.strptime(str(self.fecha_entrada),formato)
            f2=datetime.datetime.strptime(str(self.fecha_salida),formato)
            result=f1-f2
            self.dias=result.days
            self.cantidad_horas=str(result.days*8)+":00:00"

        super(SolicitudPermiso, self).save()


