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
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
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
