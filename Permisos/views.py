import requests.utils
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Permisos.models import *
from solicitudes.snniper import sumatoriaHoras, estadistica_mes, estadistica_dias, render_to_pdf, generarCodigoQR, \
    generarCodigoQRJefe


def logout_(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect("/")

def login_(request):
    if request.POST:
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'),is_active=True)
        if user:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            pass
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        return render(request,'login.html')

def forgot_password(request):
    if request.POST and not request.GET.get('username'):
        usuario=User.objects.get(username=request.POST.get('username'))
        if usuario:
            messages.add_message(request, messages.SUCCESS, 'Se ha localizado el usuario..!')
            return HttpResponseRedirect('/forgot_password/?username=%s'%usuario.username)
    if request.GET.get('username'):
        if request.POST:
            if request.POST.get('password1')==request.POST.get('password2'):
                usuario = User.objects.get(username=request.GET.get('username'))
                usuario.set_password(request.POST.get('password1'))
                usuario.save()
                messages.add_message(request, messages.SUCCESS, 'La contraseña se restableció con exito..!')
                print("Cambio exitoso")
            else:
                messages.add_message(request, messages.ERROR, 'Error, revise si las contraseñas coinciden..!')
        return render(request,'recover-password.html')
    else:
        return render(request,'forgot-password.html')

def register(request):
    if request.POST:
        try:
            user=User.objects.create_user(
                username=request.POST.get('cedula'),
                first_name=request.POST.get('nombres'),
                last_name=request.POST.get('apellidos'),
                is_active=True,
            )
            user.set_password(request.POST.get('password'))
            user.save()
            messages.add_message(request,messages.SUCCESS,'Registro creado exitosamente..!')
        except:
            messages.add_message(request, messages.ERROR, 'Lo sentimos es posible que el usuario ya este registrado, Intente nuevamente..!')
    return render(request,'register.html')
    #return render_to_pdf('register.html',{})




@login_required(login_url='login')
def index(request):
    estadistica=[]
    dias=[]
    solicitudes = SolicitudPermiso.objects.all()
    if request.user.is_staff:
        if request.GET.get("anio"):
            solicitudes = solicitudes.filter(fecha_salida__year=request.GET.get("anio"))
        else:
            solicitudes = solicitudes.filter(fecha_salida__year=datetime.datetime.now().year)
        estadistica = estadistica_mes(solicitudes)
        dias = estadistica_dias(solicitudes)

    else:
        solicitudes = solicitudes.filter(persona__user=request.user)
        if request.GET.get("anio"):
            estadistica=estadistica_mes(solicitudes,request.GET.get("anio"))
            dias=estadistica_dias(solicitudes,request.GET.get("anio"))
        else:
            estadistica=estadistica_mes(solicitudes)
            dias=estadistica_dias(solicitudes)
        try:
            funcionario=Funcionarios.objects.get(user=request.user)
            request.session['cargo']=funcionario.cargo
            request.session['direccion'] =funcionario.direccion
            request.session['jefe'] =funcionario.jefe_inmediato
            request.session['id']=Funcionarios.objects.get(user_id=request.user.id).id
        except:
            pass
    contarHOras = solicitudes.aggregate(Sum('dias'))
    if contarHOras['dias__sum'] != None:
        request.session['dias'] = str(contarHOras['dias__sum'])
    else:
        request.session['dias'] = 0
    request.session['numero'] = solicitudes.count()
    configuracion = Configuracion.objects.last()
    request.session['director'] = configuracion.nombre_director_th
    request.session['nombres'] = request.user.first_name
    request.session['apellidos'] = request.user.last_name
    request.session['horas'] = sumatoriaHoras(solicitudes)
    request.session.save()

    contexto={
        'estadistica':estadistica,
        'anios':Anios.objects.all(),
        'dias':dias,
    }
    return render(request,'index.html',contexto)

@login_required(login_url='login')
def mis_datos(request):
    funcionario=Funcionarios()
    user=User.objects.get(username=request.user.username)
    try:
        funcionario = Funcionarios.objects.get(user=request.user)
        print(funcionario)
    except:
        pass
    if request.POST:
        user.first_name=request.POST.get('nombres')
        user.last_name = request.POST.get('apellidos')
        user.save()
        funcionario.user=request.user
        funcionario.cargo=request.POST.get('cargo')
        funcionario.direccion=request.POST.get('direccion')
        funcionario.jefe_inmediato=request.POST.get('jefe')
        funcionario.director_th = request.POST.get('directorth')
        funcionario.save()
        generarCodigoQR(funcionario.user.username, funcionario.user.first_name, funcionario.user.last_name,
                        funcionario.cargo, funcionario.direccion)
        messages.add_message(request,messages.SUCCESS,"Registro actualizado exitosamente..!")
        generarCodigoQRJefe(funcionario.jefe_inmediato, funcionario.direccion)
    request.session['cargo'] = funcionario.cargo
    request.session['direccion'] = funcionario.direccion
    request.session['jefe'] = funcionario.jefe_inmediato
    request.session['id'] = funcionario.id
    request.session['nombres']=user.first_name
    request.session['apellidos'] = user.last_name
    request.session.save()

    return render(request,'misDatos.html')

@login_required(login_url='login')
def solicitud_permisos(request):
    solicitudes=SolicitudPermiso.objects.all()
    if request.user.is_staff:
        if request.GET.get("anio"):
            solicitudes=solicitudes.filter(fecha_salida__year=request.GET.get("anio"))
        else:
            solicitudes = solicitudes.filter(fecha_salida__year=datetime.datetime.now().year)
    else:
        solicitudes=solicitudes.filter(persona__user=request.user,fecha_salida__year=datetime.datetime.now().year)
        if request.GET.get("anio"):
            solicitudes = solicitudes.filter(persona__user=request.user,fecha_salida__year=request.GET.get("anio"))
        try:
            request.session['id']=Funcionarios.objects.get(user_id=request.user.id).id
        except:
            return HttpResponseRedirect("/datos/")
        if request.POST:
            print(request.POST)
            try:
                motivo=""
                sol=SolicitudPermiso()
                sol.persona_id=request.session['id']
                if request.POST.get('radio1')=="p":
                    sol.particular=True
                elif request.POST.get('radio1')=="cd":
                    sol.calamidad_domestica=True
                elif request.POST.get('radio1')=="e":
                    sol.enfermedad=True
                else:
                    sol.otros=True
                if request.POST.get('fsalida'):
                    sol.fecha_salida=request.POST.get('fsalida')
                if request.POST.get('fentrada'):
                    sol.fecha_entrada=request.POST.get('fentrada')
                if request.POST.get('hsalida'):
                    sol.hora_salida=request.POST.get('hsalida')+":00"
                if request.POST.get('hentrada'):
                    sol.hora_entrada=request.POST.get('hentrada')+":00"
                sol.otro=request.POST.get('otro')
                sol.observaciones=request.POST.get('observacion')
                sol.save()
                request.session['numero'] = solicitudes.count()
                messages.add_message(request,messages.SUCCESS,"La solicitud se ha creado exitosamente..!")
            except Exception as error:
                print(error)
    request.session['numero'] = solicitudes.count()
    contarHOras=solicitudes.aggregate(Sum('dias'))
    request.session['horas']=sumatoriaHoras(solicitudes)
    if contarHOras['dias__sum']!=None:
        request.session['dias'] = str(contarHOras['dias__sum'])
    else:
        request.session['dias'] =0

        request.session.save()
    contexto={
        'solicitudes':solicitudes,
        'anios':Anios.objects.all(),
    }
    return render(request,'solicitudPermiso.html',contexto)

def solicitudesPermisosFuncionario(request):
    permisos = SolicitudPermiso.objects.all()
    if request.GET.get('cedula'):
        request.session['cedula']=request.GET.get('cedula')

    if request.GET.get('anio'):
        request.session['anio'] = request.GET.get('anio')
    else:
        request.session['anio']=datetime.datetime.now().year

    if request.GET.get('todos'):
        request.session['cedula']=""
        request.session['anio'] = datetime.datetime.now().year

    request.session.save()

    if request.session.get('cedula'):
         permisos = permisos.filter(persona__user__username=request.session.get('cedula'),fecha_salida__year=request.session.get('anio'))

    if request.session['anio']:
        permisos = permisos.filter(fecha_salida__year=request.session['anio'])

    request.session.save()
    funcionarios = Funcionarios.objects.all().order_by('user__last_name')
    contexto={
        'funcionarios':funcionarios,
        'anios':Anios.objects.all(),
        'dias':estadistica_dias(permisos)

    }
    return render(request,'solicitudPermisoFuncionario.html',contexto)


def permiso_pdf(request,id):
    contexto={
        'permiso':SolicitudPermiso.objects.get(id=id),
    }
    #return render(request,'permisopdf.html',contexto)
    return render_to_pdf('permisopdf.html',contexto)

def solicitud_materiales(request):
    return render(request,'index.html')