from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#--->Importamos el Formulario
from .formularios import *
from .models import *

from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages
# Create your views here.
def Home(request):
    buscar=Productos.objects.all().order_by('-Codigo')[:4]
    data={
        'forms':buscar
    }
    return render(request,'index.html',data)

def Ver_Producto(request):
    # Obtener todos los productos
    productos = Productos.objects.all()

    # Configura el número de productos por página
    paginator = Paginator(productos, 5)  # Cambia '5' por el número de productos que quieras por página

    # Obtener el número de página desde la URL
    page = request.GET.get('page')

    try:
        # Obtener los productos de la página solicitada
        productos_pagina = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostramos la primera página
        productos_pagina = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostramos la última página
        productos_pagina = paginator.page(paginator.num_pages)

    # Pasar los productos paginados al contexto
    data = {
        'products': productos_pagina
    }

    return render(request, 'Productos.html', data)

def producto(request,Codigo):
 buscar=Productos.objects.filter(Codigo=Codigo)
 data={
        'mas':buscar
    }
 return render(request,'producto.html',data)

def Nosotros(request):
    return render(request, 'nosotros.html')

def register(request):
    data={
        'form':Nuevo_Usuario()
    }
    if request.method=='POST':
        data={
        'forms':Nuevo_Usuario()
    }
    if request.method=='POST':
        query=Nuevo_Usuario(data=request.POST)
        if  query.is_valid():
            query.save()
            usuario=authenticate(username=query.cleaned_data['username'],password=query.cleaned_data['password1'])
            login(request,usuario)
            data['mensaje']="Datos Registrados"
            return redirect(to='Home')
        else:
            data['forms']=query
    return render(request, 'registration.html', data)

@login_required

def perfil(request):
    user_permissions = request.user.get_all_permissions()
    return render(request,'perfil.html', {'user_permissions': user_permissions})

def permisos(request):
    data={
        'form':Nuevos_Permisos
    }
    if request.method=='POST':
        data={
        'forms':Nuevos_Permisos()
    }
    if request.method=='POST':
        query=Nuevos_Permisos(data=request.POST)
        if  query.is_valid():
            query.save()
            data['mensaje']="Datos Registrados"
        else:
            data['forms']=query
        
    return render(request, 'permisos.html',data)

def Stock(request):
        productos = Productos.objects.all()  # Obtener todos los productos
        productos_stock_bajo = productos.filter(Cantidad__lt= 10)  # Filtrar productos con stock menor a 10

        return render(request, 'productos.html', {
            'productos': productos,
            'productos_stock_bajo': productos_stock_bajo
        })

@permission_required('Sistemas.add_Productos')
def Agregar(request):
    data={
        'forms':Nuevo_Producto()
    }
    if request.method=='POST':
        query=Nuevo_Producto(data=request.POST, files=request.FILES)
        if query.is_valid():
            query.save()
            messages.success(request, "Producto añadido correctamente.")
        else:
            data['forms']=Nuevo_Producto
    return render (request,'agregar.html',data)

@permission_required('Sistemas.change_productos')
def Modificar_Producto(request,Codigo):
    sql=get_object_or_404(Productos,Codigo=Codigo)
    data={
        'forms':Nuevo_Producto(instance=sql)
    }
    if request.method=='POST':
        query=Nuevo_Producto(data=request.POST,instance=sql,files=request.FILES)
        if query.is_valid():
            sql.save()
            messages.info(request, "Producto modificado correctamente.")
            return redirect(to="productos")
        else:
            data['forms']=Nuevo_Producto
    return render (request,'modificar.html',data)

@permission_required('Sistemas.delete_productos')
def Eliminar_Producto(request,Codigo):
    buscar=get_object_or_404(Productos, Codigo=Codigo)
    buscar.delete()
    messages.error(request, "Producto eliminado correctamente.")
    return redirect(to="productos")

def Salir(request):
    logout(request)
    return redirect(to='Home')

def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(user=request.user)
    carrito_items = CarritoItem.objects.filter(carrito=carrito)
    
    # Calcular el total del carrito y los subtotales de cada item
    total = sum(item.total_precio() for item in carrito_items)
    
    context = {
        'carrito': carrito_items,
        'total': total,
    }
    return render(request, 'ver_carrito.html', context)


@login_required
def agregar_al_carrito(request, Codigo):
    producto = get_object_or_404(Productos, Codigo=Codigo)
    
    # Verifica si hay suficiente stock
    if producto.Cantidad > 0:
        carrito, created = Carrito.objects.get_or_create(user=request.user)
        carrito_item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

        if not item_created:
            carrito_item.cantidad += 1
        carrito_item.save()
        
        # Disminuir el stock del producto en 1
        producto.Cantidad -= 1
        producto.save()
        
        messages.success(request, "Producto añadido al carrito.")
    else:
        messages.error(request, "Este producto está agotado.")
    
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, Codigo):
    carrito = get_object_or_404(Carrito, user=request.user)
    carrito_item = get_object_or_404(CarritoItem, carrito=carrito, producto__Codigo=Codigo)
    carrito_item.delete()
    return redirect('ver_carrito')

