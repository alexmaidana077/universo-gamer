from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Productos (models.Model):
    Codigo=models.AutoField(primary_key=True)
    Nombre=models.TextField(max_length=60)
    Descripcion=models.TextField()
    MicroDescripcion=models.TextField(max_length=200)

    Cantidad=models.IntegerField()
    Precio=models.FloatField()
    Imagen=models.ImageField(upload_to="Productos", null=True)

    def __int__(self):
        return int(self.Codigo)

class Carrito(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def total_precio(self):
        return self.producto.Precio * self.cantidad