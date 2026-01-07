from django import forms
from .models import Solicitud
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'tipo_tramite',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'curp',
            'correo',
            'whatsapp',
            'datos_extra'
        ]

class RegistroForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario'}))
    email = forms.EmailField(label="Correo electrónico",
                             widget=forms.EmailInput(attrs={'placeholder': 'tu@email.com'}))
    password1 = forms.CharField(label="Contraseña",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label="Confirmar contraseña",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repite tu contraseña'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-input'}))