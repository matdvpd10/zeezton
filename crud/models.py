from django.db import models



class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='subcategorias'
    )

    nombre = models.CharField(max_length=100)

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        unique_together = ('categoria', 'nombre')

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )

    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos'
    )

    destacado = models.BooleanField(default=False)
    oferta = models.BooleanField(default=False)
    super_oferta = models.BooleanField(default=False, verbose_name="¿Es Super Oferta?")
    precio = models.PositiveIntegerField()
    calificacion = models.DecimalField(
    max_digits=2,
    decimal_places=1,
    default=0,
    help_text="Calificación del producto de 0.0 a 5.0"
)
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


from crud.models import Producto
from django.db import models, transaction
from django.core.exceptions import ValidationError

class MovimientoInventario(models.Model):
    COMPRA = "COMPRA"
    VENTA = "VENTA"
    TIPOS = [
        (COMPRA, "Compra"),
        (VENTA, "Venta"),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    referencia = models.CharField(max_length=120, blank=True)
    nota = models.TextField(blank=True)
    total = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.get_tipo_display()} #{self.id}"

    def recalcular_total(self):
        total = 0
        for d in self.detalles.all():
            total += (d.cantidad * d.precio_unitario)
        self.total = total
        self.save(update_fields=["total"])


class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(
        MovimientoInventario,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
    Producto,
    on_delete=models.PROTECT,
    related_name="detalles_movimiento_crud"
)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.full_clean()

        mov = MovimientoInventario.objects.select_for_update().get(pk=self.movimiento_id)

        # Estado anterior
        if self.pk:
            prev = DetalleMovimiento.objects.select_for_update().get(pk=self.pk)
            prev_producto_id = prev.producto_id
            prev_cantidad = prev.cantidad
        else:
            prev_producto_id = None
            prev_cantidad = 0

        super().save(*args, **kwargs)

        # Si cambió el producto, revertir efecto en el anterior
        if prev_producto_id and prev_producto_id != self.producto_id:
            prod_prev = Producto.objects.select_for_update().get(pk=prev_producto_id)

            if mov.tipo == MovimientoInventario.COMPRA:
                prod_prev.stock -= prev_cantidad
            else:
                prod_prev.stock += prev_cantidad

            if prod_prev.stock < 0:
                raise ValidationError("Operación inválida: stock negativo al revertir un cambio.")
            prod_prev.save(update_fields=["stock"])

            prev_cantidad = 0

        # Aplicar delta al producto actual
        prod = Producto.objects.select_for_update().get(pk=self.producto_id)
        delta = self.cantidad - prev_cantidad

        if mov.tipo == MovimientoInventario.COMPRA:
            prod.stock += delta
        else:
            if prod.stock < delta:
                raise ValidationError(f"Stock insuficiente para {prod.nombre}. Disponible: {prod.stock}")
            prod.stock -= delta

        if prod.stock < 0:
            raise ValidationError("Operación inválida: stock negativo.")
        prod.save(update_fields=["stock"])

        mov.recalcular_total()

    @transaction.atomic
    def delete(self, *args, **kwargs):
        mov = MovimientoInventario.objects.select_for_update().get(pk=self.movimiento_id)
        prod = Producto.objects.select_for_update().get(pk=self.producto_id)

        if mov.tipo == MovimientoInventario.COMPRA:
            prod.stock -= self.cantidad
        else:
            prod.stock += self.cantidad

        if prod.stock < 0:
            raise ValidationError("Operación inválida: stock negativo al eliminar.")
        prod.save(update_fields=["stock"])

        super().delete(*args, **kwargs)
        mov.recalcular_total()



class ImagenProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='productos/galeria/')
    principal = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', 'id']

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

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