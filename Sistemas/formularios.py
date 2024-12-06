from django import forms
from .models import *

from django.forms import ValidationError
#--->Importacion del Modelo--> Traemos algunos Campos
from django.contrib.auth.models import User
#---> Que es la tabla  a trabajar
from django.contrib.auth.forms import UserCreationForm

class Nuevo_Producto(forms.ModelForm):
    class Meta:
        model=Productos
        fields='__all__'

class Nuevo_Usuario(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name','username',"email","password1","password2"]

class Nuevos_Permisos(UserCreationForm):
    class Meta:
        model=User
        fields=['username',"email","password1","password2","is_staff","is_superuser","user_permissions"]