from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Solicitud
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm, LoginForm, SolicitudForm
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings



def inicio(request):
    return render(request, 'app/inicio.html')

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        # Intentar autenticar por username
        user = authenticate(request, username=username_or_email, password=password)

        # Si no funciona, intentar con email
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "app/login.html")


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            try:
                # Crear usuario usando el username proporcionado
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)  # Inicia sesión automáticamente
                messages.success(request, "¡Registro exitoso!")
                return redirect('dashboard')
            except IntegrityError:
                # Esto debería raramente ocurrir porque ya validamos username y email
                form.add_error(None, "Hubo un error al registrar el usuario.")
    else:
        form = RegistroForm()

    return render(request, 'app/registro.html', {'form': form})

def dashboard(request):
    return render(request, 'app/dashboard.html')

@login_required
def solicitar_tramite(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user
            solicitud.save()

            
            # 📧 ENVÍO DE CORREO
            send_mail(
                subject='📄 Trámite recibido - PuntoZero',
                message=f'''
                Hola {solicitud.nombre},

                Recibimos tu solicitud correctamente.

                📌 Trámite: {solicitud.tipo_tramite}
                🆔 CURP: {solicitud.curp}
                📧 Correo: {solicitud.correo}
                📞 WhatsApp: {solicitud.whatsapp}

                Nos pondremos en contacto contigo para darle seguimiento.

                Gracias por usar PuntoZero.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return redirect('mis_solicitudes')
    else:
        form = SolicitudForm()

    return render(request, 'app/solicitar.html', {'form': form})
from .models import Solicitud

@login_required
def mis_solicitudes(request):
    solicitudes = Solicitud.objects.filter(usuario=request.user)
    return render(request, 'app/mis_solicitudes.html', {'solicitudes': solicitudes})


def logout_view(request):
    logout(request)
    return render(request, 'app/inicio.html')
