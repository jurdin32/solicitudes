from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from Permisos.models import *
from solicitudes.snniper import sumatoriaHoras, estadistica_mes, estadistica_dias


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




@login_required(login_url='login')
def index(request):
    solicitudes=SolicitudPermiso.objects.filter(persona__user=request.user)
    estadistica=[]
    dias=[]
    if request.GET.get("anio"):
        estadistica=estadistica_mes(solicitudes,request.GET.get("anio"))
        dias=estadistica_dias(solicitudes,request.GET.get("anio"))
    else:
        estadistica=estadistica_mes(solicitudes)
        dias=estadistica_dias(solicitudes)
    configuracion = Configuracion.objects.last()
    request.session['director']=configuracion.nombre_director_th
    request.session['nombres'] = request.user.first_name
    request.session['apellidos'] = request.user.last_name
    try:
        funcionario=Funcionarios.objects.get(user=request.user)
        request.session['cargo']=funcionario.cargo
        request.session['direccion'] =funcionario.direccion
        request.session['jefe'] =funcionario.jefe_inmediato
        request.session['id']=Funcionarios.objects.get(user_id=request.user.id).id
    except:
        pass
    try:
        if request.GET.get("anio"):
            solicitudes=solicitudes.filter(fecha__month=datetime.datetime.now().month,fecha__year=request.GET.get("anio"))
        else:
            solicitudes = solicitudes.filter(fecha__month=datetime.datetime.now().month, fecha__year=datetime.datetime.now().year)
        request.session['numero']=solicitudes.count()
        contarHOras=solicitudes.aggregate(Sum('dias'))
        request.session['horas']=sumatoriaHoras(solicitudes)
        request.session['dias'] = str(contarHOras['dias__sum'])
    except Exception as error:
        print(error)
    request.session.save()
    print(Anios.objects.all())
    contexto={
        'estadistica':estadistica,
        'anios':Anios.objects.all(),
        'dias':dias,
    }
    return render(request,'index.html',contexto)

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
        funcionario.save()
        messages.add_message(request,messages.SUCCESS,"Registro actualizado exitosamente..!")
    request.session['cargo'] = funcionario.cargo
    request.session['direccion'] = funcionario.direccion
    request.session['jefe'] = funcionario.jefe_inmediato
    request.session['id'] = funcionario.id
    request.session['nombres']=user.first_name
    request.session['apellidos'] = user.last_name
    request.session.save()
    return render(request,'misDatos.html')

def solicitud_permisos(request):
    try:
        request.session['id']=Funcionarios.objects.get(user_id=request.user.id).id
    except:
        return HttpResponseRedirect("/datos/")
    if request.POST:
        print(request.POST)
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
        messages.add_message(request,messages.SUCCESS,"La solicitud se ha creado exitosamente..!")
    try:
        solicitudes=SolicitudPermiso.objects.filter(persona__user=request.user,fecha__month=datetime.datetime.now().month)
        request.session['numero'] = solicitudes.count()
        contarHOras=solicitudes.aggregate(Sum('dias'))
        request.session['horas']=sumatoriaHoras(solicitudes)
        request.session['dias'] = str(contarHOras['dias__sum'])
    except Exception as error:
        print(error)

    contexto={
        'solicitudes':SolicitudPermiso.objects.filter(persona_id=request.session['id'])
    }
    return render(request,'solicitudPermiso.html',contexto)

def solicitud_materiales(request):
    return render(request,'index.html')

colores=['rgb(165, 42, 42)','rgb(255, 248, 220)','	rgb(0, 0, 139)','	rgb(139, 0, 139)']