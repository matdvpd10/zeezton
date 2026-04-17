from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    destacado = models.BooleanField(default=False)
    oferta = models.BooleanField(default=False)
    super_oferta = models.BooleanField(default=False, verbose_name="¿Es Super Oferta?")

    precio = models.PositiveIntegerField()
    costo_promedio = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    orden = models.PositiveIntegerField(default=0)
    orden_destacado = models.PositiveIntegerField(default=0)

    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="productos")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return self.nombre

# 🔹 Nuevo modelo para reseñas generales de la página
class Reseña(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)   # Nuevo campo
    comentario = models.TextField()
    calificacion = models.IntegerField(
        choices=[(i, f"{i} ★") for i in range(1, 6)],
        default=5
    )
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.calificacion}★"