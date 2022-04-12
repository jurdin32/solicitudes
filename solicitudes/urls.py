from django.contrib import admin
from django.urls import path

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
    path('documento/<int:id>/',permiso_pdf, name='documento'),

    path('materiales/',solicitud_materiales, name='materiales'),
]
