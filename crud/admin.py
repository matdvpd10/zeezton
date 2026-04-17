from django.contrib import admin
from .models import Marca, Producto, Reseña


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado")
    search_fields = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "marca",
        "precio",          # precio de venta
        "costo_promedio",  # costo real calculado
        "ganancia_unitaria",
        "stock",
        "ganancia_total_stock",
        "oferta",
        "super_oferta",
        "destacado",
        "orden",

    )

    list_filter = ("marca", "oferta")
    search_fields = ("nombre", "marca__nombre")
    ordering = ("orden", "nombre")
    list_editable = ("orden", "oferta","super_oferta","destacado")

    def ganancia_unitaria(self, obj):
        return obj.precio - obj.costo_promedio
    ganancia_unitaria.short_description = "Ganancia unit."

    def ganancia_total_stock(self, obj):
        return (obj.precio - obj.costo_promedio) * obj.stock
    ganancia_total_stock.short_description = "Ganancia stock"

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "calificacion", "creado")
    search_fields = ("nombre", "comentario")
    list_filter = ("calificacion",)
