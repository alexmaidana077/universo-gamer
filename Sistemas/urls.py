from django.urls import path
from .views import *

urlpatterns = [
    path('',Home, name='Home'),
    path('agregar/',Agregar,name='agregar'),
    path('productos/', Ver_Producto, name='productos'),
    path('eliminar/<Codigo>/', Eliminar_Producto,name='eliminar'),
    path('modificar/<Codigo>/', Modificar_Producto, name='modificar'),
    path('producto/<Codigo>/', producto, name='producto'),
    path('agregar_al_carrito/<Codigo>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<Codigo>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('menos_del_carrito/<Codigo>/', menos_del_carrito, name='menos_del_carrito'),
    path('mas_del_carrito/<Codigo>/', mas_del_carrito, name='mas_del_carrito'),
    path('eliminar_carrito/', Eliminar_carrito, name='eliminar_carrito'),
    path('logouts/',Salir,name='logouts'),
    path('registro/',register,name='registro'),
    path('nosotros/',Nosotros,name='nosotros'),
    path('permisos/', permisos, name='permisos'),
    path('perfil/', perfil, name='perfil'),
    path('boleta/',Boleta,name='boleta'),
]
