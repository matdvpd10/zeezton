from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crud.models import Producto, Marca, Reseña
from crud.forms import ReseñaForm

import unicodedata
import json

def root(request):
    return redirect('home')


def home(request):
    return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == "POST":
        form = ReseñaForm(request.POST)
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.aprobada = False
            reseña.save()
            return redirect("contact")
    else:
        form = ReseñaForm()

    reseñas = Reseña.objects.filter(aprobada=True).order_by("-creado")[:5]
    return render(request, 'core/contact.html', {"form": form, "reseñas": reseñas})


def product(request):
    buscar = request.GET.get("buscar", "").strip()
    marca_id = request.GET.get("marca", "").strip()

    productos_qs = Producto.objects.all().order_by("-id")

    if buscar:
        texto = quitar_tildes(buscar).lower()
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=texto) |
            Q(descripcion__icontains=texto) |
            Q(marca__nombre__icontains=texto)
        ).distinct()

    if marca_id:
        productos_qs = productos_qs.filter(marca__id=marca_id)

    # 🔥 TOP 5 DESTACADOS (independiente de filtros)
    productos_destacados = Producto.objects.filter(destacado=True).order_by("-id")[:10]

    paginator = Paginator(productos_qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    marcas = Marca.objects.all()

    context = {
        "page_obj": page_obj,
        "productos": page_obj.object_list,
        "marcas": marcas,
        "buscar": buscar,
        "marca_seleccionada": marca_id,
        "total_resultados": productos_qs.count(),
        "productos_destacados": productos_destacados,
    }
    return render(request, "core/product.html", context)


def product_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'core/product_detail.html', {"producto": producto})


def offers(request):
    # Trae todos los productos en oferta para la grilla normal
    productos = Producto.objects.filter(oferta=True)

    # 🔥 AQUI ESTÁ EL CAMBIO: Filtramos SOLO los que marcaste como super_oferta
    productos_super_ofertas = Producto.objects.filter(super_oferta=True)

    context = {
        'productos': productos,
        'productos_super_ofertas': productos_super_ofertas,
    }
    return render(request, 'core/ofertas.html', context)


def quitar_tildes(texto):
    if not texto:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )

def api_productos(request):
    productos = []

    qs = Producto.objects.select_related("marca").all().order_by("id")

    for p in qs:
        imagen_url = request.build_absolute_uri(p.imagen.url) if p.imagen else ""

        productos.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion or "",
            "precio": p.precio,
            "stock": p.stock,
            "marca": p.marca.nombre if p.marca else "",
            "imagen": imagen_url,
            "destacado": p.destacado,
            "oferta": p.oferta,
            "super_oferta": p.super_oferta,
        })

    return JsonResponse(productos, safe=False)

@csrf_exempt
def vender_producto(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        producto_id = data.get("producto_id")
        cantidad = data.get("cantidad")

        if not producto_id or not cantidad:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

        if cantidad <= 0:
            return JsonResponse({"error": "Cantidad inválida"}, status=400)

        producto = Producto.objects.get(id=producto_id)

        if producto.stock < cantidad:
            return JsonResponse({"error": "Stock insuficiente"}, status=400)

        # 🔥 RESTAR STOCK DIRECTAMENTE
        producto.stock -= cantidad
        producto.save()

        return JsonResponse({
            "mensaje": "Venta realizada correctamente",
            "nuevo_stock": producto.stock
        })

    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def api_producto_detalle(request, pk):
    try:
        p = Producto.objects.select_related("marca").get(pk=pk)
    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    imagen_url = request.build_absolute_uri(p.imagen.url) if p.imagen else ""

    producto = {
        "id": p.id,
        "nombre": p.nombre,
        "descripcion": p.descripcion or "",
        "precio": p.precio,
        "stock": p.stock,
        "marca": p.marca.nombre if p.marca else "",
        "imagen": imagen_url,
        "destacado": p.destacado,
        "oferta": p.oferta,
        "super_oferta": p.super_oferta,
    }

    return JsonResponse(producto, safe=False)



