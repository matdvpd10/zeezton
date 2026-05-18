from django.contrib import admin
from .models import Marca, Producto, Reseña, Cliente, Venta, DetalleVenta
from .models import Suscriptor
from .models import Producto, Marca, Categoria, Subcategoria, ImagenProducto


class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1

# ---------------- MARCA ----------------
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "creado", "actualizado")
    search_fields = ("nombre",)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria__nombre')

# ---------------- PRODUCTO ----------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [ImagenProductoInline]

    list_display = (
    
        "nombre",
        "marca",
        "precio",
        "calificacion",
        "costo_promedio",
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
    list_editable = ("orden", "oferta", "super_oferta", "destacado")

    def ganancia_unitaria(self, obj):
        return obj.precio - obj.costo_promedio
    ganancia_unitaria.short_description = "Ganancia unit."

    def ganancia_total_stock(self, obj):
        return (obj.precio - obj.costo_promedio) * obj.stock
    ganancia_total_stock.short_description = "Ganancia stock"


# ---------------- RESEÑA ----------------
@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "calificacion", "aprobada", "creado")
    search_fields = ("nombre", "comentario")
    list_filter = ("calificacion", "aprobada", "creado")
    list_editable = ("aprobada",)

    actions = ["aprobar_reseñas"]

    def aprobar_reseñas(self, request, queryset):
        queryset.update(aprobada=True)

    aprobar_reseñas.short_description = "Aprobar reseñas seleccionadas"


# ---------------- CLIENTE ----------------
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'numero_documento',
        'nombre',
        'apellido',
        'rut',
        'telefono',
        'email',
        'comuna',
        'creado',
    )

    search_fields = (
        'numero_documento',
        'nombre',
        'apellido',
        'rut',
        'telefono',
        'email',
        'comuna',
    )

    list_filter = (
        'comuna',
        'creado',
    )

    readonly_fields = (
        'creado',
        'actualizado',
    )

    fieldsets = (
        ('Información Cliente', {
            'fields': (
                'nombre',
                'apellido',
                'fecha_nacimiento',
                'rut',
                'email',
                'telefono',
                'numero_documento',
            )
        }),
        ('Información Entrega', {
            'fields': (
                'direccion',
                'numero',
                'comuna',
                'departamento',
                'informacion_adicional',
            )
        }),
        ('Fechas del sistema', {
            'fields': (
                'creado',
                'actualizado',
            )
        }),
    )

@admin.register(Suscriptor)
class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ('email', 'nombre', 'marca', 'modelo', 'creado')
    search_fields = ('email', 'nombre', 'modelo')
    list_filter = ('marca', 'creado')

# 🔥 INLINE DETALLE VENTA (esto es clave)
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


# ---------------- VENTA ----------------
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "tipo_documento", "total", "fecha")
    list_filter = ("tipo_documento", "fecha")
    search_fields = ("cliente__nombre", "cliente__apellido", "cliente__numero_documento")
    inlines = [DetalleVentaInline]


# ---------------- DETALLE VENTA ----------------
@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("venta", "producto", "cantidad", "precio_unitario", "subtotal")
    search_fields = ("producto__nombre",)