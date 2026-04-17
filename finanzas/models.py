from django.db import models
from crud.models import Producto


class Proveedor(models.Model):
    nombre = models.CharField(max_length=120)
    contacto = models.CharField(max_length=200)  # WhatsApp / teléfono / email
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.contacto})"


class Compra(models.Model):
    ESTADOS = (
        ("BORRADOR", "Borrador"),
        ("CONFIRMADA", "Confirmada"),
    )

    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    impuesto_total = models.PositiveIntegerField(default=0)
    envio_total = models.PositiveIntegerField(default=0)
    otros_costos = models.PositiveIntegerField(default=0)

    estado = models.CharField(max_length=12, choices=ESTADOS, default="BORRADOR")

    def __str__(self):
        return f"Compra #{self.id} - {self.estado}"

    def extras_total(self):
        return self.impuesto_total + self.envio_total + self.otros_costos

    def confirmar(self):
        if self.estado == "CONFIRMADA":
            return

        items = list(self.items.select_related("producto"))
        if not items:
            raise ValueError("No puedes confirmar una compra sin items.")

        subtotal_total = sum(i.subtotal_base() for i in items)
        if subtotal_total <= 0:
            raise ValueError("Subtotal inválido. Revisa costos/cantidades.")

        factor = (subtotal_total + self.extras_total()) / subtotal_total

        for item in items:
            costo_unit_real = round(item.costo_unit_base * factor)
            item.costo_unit_real = costo_unit_real
            item.save(update_fields=["costo_unit_real"])

            p = item.producto
            stock_anterior = p.stock
            stock_nuevo = stock_anterior + item.cantidad

            costo_total_anterior = p.costo_promedio * stock_anterior
            costo_total_nuevo = costo_unit_real * item.cantidad

            p.costo_promedio = round((costo_total_anterior + costo_total_nuevo) / stock_nuevo)
            p.stock = stock_nuevo
            p.save(update_fields=["costo_promedio", "stock"])

        self.estado = "CONFIRMADA"
        self.save(update_fields=["estado"])


class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()

    costo_unit_base = models.PositiveIntegerField()   # CLP base
    costo_unit_real = models.PositiveIntegerField(default=0)  # CLP prorrateado

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"

    def subtotal_base(self):
        return self.costo_unit_base * self.cantidad


class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    cliente = models.CharField(max_length=120, blank=True)

    total_venta = models.PositiveIntegerField(default=0)
    total_costo = models.PositiveIntegerField(default=0)
    ganancia_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Venta #{self.id}"

    def recalcular_totales(self):
        total_venta = 0
        total_costo = 0
        for item in self.items.select_related("producto"):
            total_venta += item.precio_unitario * item.cantidad
            total_costo += item.costo_unitario * item.cantidad
        self.total_venta = total_venta
        self.total_costo = total_costo
        self.ganancia_total = total_venta - total_costo
        self.save(update_fields=["total_venta", "total_costo", "ganancia_total"])


class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)

    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField(default=0)
    costo_unitario = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.precio_unitario = self.producto.precio
            self.costo_unitario = self.producto.costo_promedio

            if self.producto.stock < self.cantidad:
                raise ValueError("Stock insuficiente para esta venta.")
            self.producto.stock -= self.cantidad
            self.producto.save(update_fields=["stock"])

        super().save(*args, **kwargs)
        self.venta.recalcular_totales()
