from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from crud.models import Producto, Marca, Reseña
from crud.forms import ReseñaForm

import unicodedata


def root(request):
    return redirect("home")


def home(request):
    return render(request, "core/index.html")


def about(request):
    return render(request, "core/about.html")


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

    return render(request, "core/contact.html", {
        "form": form,
        "reseñas": reseñas
    })


def product(request):
    buscar = request.GET.get("buscar", "").strip()
    marca_id = request.GET.get("marca", "").strip()

    productos_qs = Producto.objects.select_related(
        "marca"
    ).prefetch_related(
        "imagenes"
    ).all().order_by("-id")

    if buscar:
        texto = quitar_tildes(buscar).lower()
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=texto) |
            Q(descripcion__icontains=texto) |
            Q(marca__nombre__icontains=texto)
        ).distinct()

    if marca_id:
        productos_qs = productos_qs.filter(marca__id=marca_id)

    productos_destacados = Producto.objects.select_related(
        "marca"
    ).prefetch_related(
        "imagenes"
    ).filter(
        destacado=True
    ).order_by("-id")[:10]

    print("TOTAL PRODUCTOS:", productos_qs.count())
    print("PRODUCTOS:", list(productos_qs.values_list("id", "nombre")[:10]))

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
    producto = get_object_or_404(
        Producto.objects.select_related("marca").prefetch_related("imagenes"),
        pk=pk
    )

    imagenes = producto.imagenes.order_by("-principal", "orden", "id")
    imagen_principal = imagenes.first()

    return render(request, "core/product_detail.html", {
        "producto": producto,
        "imagenes": imagenes,
        "imagen_principal": imagen_principal,
    })


def offers(request):
    productos = Producto.objects.filter(
        oferta=True
    ).prefetch_related(
        "imagenes"
    )

    productos_super_ofertas = Producto.objects.filter(
        super_oferta=True
    ).prefetch_related(
        "imagenes"
    )

    context = {
        "productos": productos,
        "productos_super_ofertas": productos_super_ofertas,
    }

    return render(request, "core/ofertas.html", context)


def quitar_tildes(texto):
    if not texto:
        return ""

    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )