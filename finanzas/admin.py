from django.contrib import admin
from .models import Proveedor, Compra, CompraItem, Venta, VentaItem


class CompraItemInline(admin.TabularInline):
    model = CompraItem
    extra = 1
    readonly_fields = ("costo_unit_real",)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "contacto", "creado")
    search_fields = ("nombre", "contacto")


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "estado", "proveedor", "fecha_ingreso", "impuesto_total", "envio_total", "otros_costos")
    list_filter = ("estado", "proveedor", "fecha_ingreso")
    inlines = [CompraItemInline]
    readonly_fields = ("fecha_ingreso",)
    actions = ["confirmar_compras"]

    def confirmar_compras(self, request, queryset):
        for compra in queryset:
            compra.confirmar()
        self.message_user(request, "Compras confirmadas: stock y costo actualizado.")
    confirmar_compras.short_description = "Confirmar compras seleccionadas"


# -------------------
# VENTAS
# -------------------

class VentaItemInline(admin.TabularInline):
    model = VentaItem
    extra = 1
    readonly_fields = ("costo_unitario", "precio_unitario")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "cliente", "total_venta", "total_costo", "ganancia_total")
    inlines = [VentaItemInline]
    readonly_fields = ("fecha", "total_venta", "total_costo", "ganancia_total")
