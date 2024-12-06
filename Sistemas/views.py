from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#--->Importamos el Formulario
from .formularios import *
from .models import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages

from django.utils.timezone import now
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

    # Filtrar productos con stock bajo
    productos_bajo_stock = productos.filter(Cantidad__lt=15)
    nombres_bajo_stock = productos_bajo_stock.values_list('Nombre', flat=True) 

    paginator = Paginator(productos, 5)
    page = request.GET.get('page')

    try:
        productos_pagina = paginator.page(page)
    except PageNotAnInteger:
        productos_pagina = paginator.page(1)
    except EmptyPage:
        productos_pagina = paginator.page(paginator.num_pages)

    # Pasar los productos paginados al contexto
    data = {
        'products': productos_pagina
    }

    # Crear el mensaje de advertencia si hay productos con stock bajo
    if productos_bajo_stock.exists():
        nombres_lista = ', '.join(nombres_bajo_stock) # se separa la lista de nombres apartir de las comas
        messages.warning(
            request,
            f"Los siguientes productos tienen stock bajo: {nombres_lista}. Revisa los detalles."
            #se utiliza la f como una forma de cadena de formateo para los nombres de cada producto 
        )

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
    
    total = sum(item.total_precio() for item in carrito_items)
    
    context = {
        'carrito': carrito_items,
        'total': total,
    }
    return render(request, 'ver_carrito.html', context)


from django.shortcuts import redirect

@login_required
def agregar_al_carrito(request, Codigo):
    producto = get_object_or_404(Productos, Codigo=Codigo)
    
    if producto.Cantidad > 0:
        carrito, created = Carrito.objects.get_or_create(user=request.user)
        carrito_item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

        if not item_created:
            carrito_item.cantidad += 1
        carrito_item.save()
        
        producto.Cantidad -= 1
        producto.save()
        
        messages.success(request, "Producto añadido al carrito.")
    else:
        messages.error(request, "Este producto está agotado.")
    
    return redirect('productos')


@login_required
def Boleta(request):
    # Obtener el carrito del usuario
    carrito = CarritoItem.objects.filter(carrito__user=request.user)
    total = sum(item.total_precio() for item in carrito)

    # Datos del contexto
    context = {
        'user': request.user,
        'carrito': carrito,
        'total': total,
        'fecha_hora': now(),
    }

    # Cargar plantilla
    template = get_template('boleta.html')
    html = template.render(context)

    # Configurar respuesta HTTP para PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="boleta_{request.user.username}.pdf"'

    # Generar PDF con xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar errores
    if pisa_status.err:
        return HttpResponse(f"Error al generar PDF: {pisa_status.err}", content_type="text/plain")

    return response

@login_required
def eliminar_del_carrito(request, Codigo):
    carrito = get_object_or_404(Carrito, user=request.user)
    carrito_item = get_object_or_404(CarritoItem, carrito=carrito, producto__Codigo=Codigo)

    producto = carrito_item.producto

    producto.Cantidad += carrito_item.cantidad
    producto.save()

    carrito_item.delete()
    
    messages.error(request, "Producto eliminado del carrito.")
    
    return redirect('ver_carrito')

@login_required
def menos_del_carrito(request, Codigo):
    # Obtiene el carrito del usuario
    carrito = get_object_or_404(Carrito, user=request.user)
    # Busca el ítem en el carrito correspondiente al producto
    carrito_item = get_object_or_404(CarritoItem, carrito=carrito, producto__Codigo=Codigo)

    # Reduce la cantidad del producto en el carrito
    if carrito_item.cantidad > 1:
        carrito_item.cantidad -= 1
        carrito_item.save()

        # Aumenta la cantidad disponible del producto
        producto = carrito_item.producto
        producto.Cantidad += 1
        producto.save()

        messages.info(request, "Cantidad del producto reducida en el carrito.")
    else:
        # Si la cantidad es 1, elimina el ítem del carrito
        carrito_item.delete()
        messages.warning(request, "Producto eliminado del carrito.")

    return redirect('ver_carrito')

@login_required
def mas_del_carrito(request, Codigo):
    producto = get_object_or_404(Productos, Codigo=Codigo)

    if producto.Cantidad > 0:  # Verifica si hay suficiente stock
        # mantiene el carrito del usuario y modifica el de el
        carrito, created = Carrito.objects.get_or_create(user=request.user)
        # Obtiene o crea el ítem correspondiente al producto
        carrito_item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        
        # Incrementa la cantidad del ítem en el carrito
        carrito_item.cantidad += 1
        carrito_item.save()

        # Reduce la cantidad disponible del producto
        producto.Cantidad -= 1
        producto.save()

        messages.success(request, "Cantidad del producto aumentada en el carrito.")
    else:
        messages.error(request, "No hay suficiente stock para añadir más de este producto.")

    return redirect('ver_carrito')

@login_required
def Eliminar_carrito(request):
    carrito = get_object_or_404(Carrito, user=request.user)

    carrito_items = CarritoItem.objects.filter(carrito=carrito)

    for item in carrito_items:
        producto = item.producto
        producto.Cantidad += item.cantidad
        producto.save()

    carrito_items.delete()
    
    messages.error(request, "Todos los productos han sido eliminados del carrito.")
    return redirect('ver_carrito')