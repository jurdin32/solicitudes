from django.contrib import admin

# Register your models here.
from Permisos.models import *
from solicitudes.snniper import Attr

@admin.register(Anios)
class modelo(admin.ModelAdmin):
    list_display = Attr(Anios)
    list_display_links = Attr(Anios)

@admin.register(Configuracion)
class modelo(admin.ModelAdmin):
    list_display = Attr(Configuracion)
    list_display_links = Attr(Configuracion)

@admin.register(Funcionarios)
class modelo(admin.ModelAdmin):
    list_display = Attr(Funcionarios)
    list_display_links = Attr(Funcionarios)

@admin.register(SolicitudPermiso)
class modelo(admin.ModelAdmin):
    list_display = Attr(SolicitudPermiso)
    list_display_links = Attr(SolicitudPermiso)