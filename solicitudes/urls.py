from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Permisos.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('login/',login_,name='login'),
    path('logout/',logout_,name='logout'),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('register/',register,name='register'),
    path('datos/',mis_datos, name='datos'),
    path('permisos/',solicitud_permisos, name='permisos'),
    path('permisosfuncionario/',solicitudesPermisosFuncionario, name='permisosfuncionario'),
    path('documento/<int:id>/',permiso_pdf, name='documento'),
    path('materiales/',solicitud_materiales, name='materiales'),
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
