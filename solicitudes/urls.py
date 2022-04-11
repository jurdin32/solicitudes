"""solicitudes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('materiales/',solicitud_materiales, name='materiales'),
]
