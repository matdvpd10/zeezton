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


class Reseña(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    comentario = models.TextField()
    calificacion = models.IntegerField(
        choices=[(i, f"{i} ★") for i in range(1, 6)],
        default=5
    )
    creado = models.DateTimeField(auto_now_add=True)
    aprobada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.calificacion}★"


class Cliente(models.Model):
    numero_documento = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    comuna = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=50, blank=True, null=True)
    informacion_adicional = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.numero_documento} - {self.nombre or ''} {self.apellido or ''}"


class Venta(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ("BOLETA", "Boleta"),
        ("FACTURA", "Factura"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas"
    )
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Venta #{self.id} - {self.tipo_documento} - {self.total}"

    def recalcular_total(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.save(update_fields=["total"])


class Suscriptor(models.Model):
    email = models.EmailField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="detalles_venta")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Venta {self.venta.id} - {self.producto.nombre} x {self.cantidad}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class Informe(models.Model):
    TIPO_CHOICES = [
        ("Mejora", "Mejora"),
        ("Reclamo", "Reclamo"),
        ("Error del sistema", "Error del sistema"),
        ("Problema de stock", "Problema de stock"),
        ("Problema con cliente", "Problema con cliente"),
        ("Problema con venta", "Problema con venta"),
        ("Proveedor", "Proveedor"),
        ("Otro", "Otro"),
    ]

    PRIORIDAD_CHOICES = [
        ("Baja", "Baja"),
        ("Media", "Media"),
        ("Alta", "Alta"),
    ]

    ESTADO_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("En revisión", "En revisión"),
        ("Resuelto", "Resuelto"),
    ]

    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default="Baja")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.tipo} - {self.titulo}"