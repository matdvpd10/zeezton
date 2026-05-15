from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from crud.models import Producto, Marca, Reseña, Cliente, Venta, DetalleVenta, Informe
from crud.forms import ReseñaForm
import unicodedata
import json
import mercadopago
from django.shortcuts import redirect
from .models import Producto
from core.models import MovimientoInventario, DetalleMovimiento
from .models import Informe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Suscriptor
from django.db import transaction

# Create your views here.
def root(request):
    return redirect('products/')




def products_list(request):
    context = {
        "productos": Producto.objects.all().order_by('orden', 'id')
    }
    return render(request,'crud/productos.html',context)



def product_new(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST,request.FILES)
        if form.is_valid():
            id = form.cleaned_data.get('id')
            descripcion = form.cleaned_data.get('descripcion')
            marca = form.cleaned_data.get('marca')
            precio = form.cleaned_data.get('precio')
            stock = form.cleaned_data.get('stock')
            imagen = form.cleaned_data.get('imagen')
            obj = Producto.objects.create(
                id=id,
                descripcion=descripcion,
                marca=marca,
                precio=precio,
                stock=stock,
                imagen=imagen
            )
            obj.save()
            return redirect(reverse('product-list')+'?CREATED')
        else:
            return redirect(reverse('product-list')+'?FAIL')
    else:
        context = {
            "form": ProductoForm
        }
        return render(request,'crud/producto-new.html',context)

def product_offers(request):
    try:
        context = {
            "productos": Producto.objects.filter(oferta=True).order_by('orden', 'id')
        }
        return render(request, 'crud/ofertas.html', context)
    except:
        return redirect(reverse('product-list') + '?FAIL')


def product_detail(request,product_id):
    try:
        context = {
            "producto" : Producto.objects.get(id=product_id)
        }
        return render(request,'crud/producto-detail.html',context)
    except:
        return redirect(reverse('product-list')+'?NOT_FOUND')

def product_edit(request,product_id):
    producto = Producto.objects.get(id=product_id)
    if producto:
        form = ProductoForm(instance=producto)
    else:
        return redirect(reverse('product-list')+ '?FAIL')

    if request.method == 'POST':
        form = ProductoForm(request.POST,request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect(reverse('product-list') + '?UPDATED')
        else:
            return redirect(reverse('product-edit') + product_id)

    context = {
        'form':form
        }
    return render(request,'crud/producto-edit.html',context)


def product_delete(request,product_id):
    try:
        producto = Producto.objects.get(id=product_id)
        if producto:
            producto.delete()
            return redirect(reverse('product-list') + '?DELETED')
        else:
            return redirect(reverse('product-list') + '?NOT_FOUND')
    except:
        return redirect(reverse('product-list') + '?FAIL')

def product_by_marca(request, marca):
    try:
        context = {
            "productos": Producto.objects.filter(marca=marca).order_by('orden', 'id')
        }
        return render(request, 'crud/productos.html', context)
    except:
        return redirect(reverse('product-list') + '?FAIL')






@csrf_exempt
def crear_venta(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        tipo_documento = data.get("tipo_documento")
        detalles = data.get("detalles", [])
        cliente_id = data.get("cliente_id")

        if not tipo_documento:
            return JsonResponse({"error": "Falta tipo_documento"}, status=400)

        if tipo_documento not in ["BOLETA", "FACTURA"]:
            return JsonResponse({"error": "Tipo de documento inválido"}, status=400)

        if not detalles:
            return JsonResponse({"error": "La venta no tiene productos"}, status=400)

        if not cliente_id:
            return JsonResponse({"error": "Falta cliente_id"}, status=400)

        cliente = Cliente.objects.get(id=cliente_id)

        with transaction.atomic():
            venta = Venta.objects.create(
                cliente=cliente,
                tipo_documento=tipo_documento
            )

            for item in detalles:
                producto_id = item.get("producto_id")
                cantidad = item.get("cantidad")

                if not producto_id or not cantidad:
                    raise ValueError("Detalle incompleto")

                cantidad = int(cantidad)

                if cantidad <= 0:
                    raise ValueError("Cantidad inválida")

                producto = Producto.objects.select_for_update().get(id=producto_id)

                if producto.stock < cantidad:
                    raise ValueError(f"Stock insuficiente para {producto.nombre}")

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

                # ✅ AQUÍ SE DESCUENTA AUTOMÁTICAMENTE EL STOCK
                producto.stock -= cantidad
                producto.save(update_fields=["stock"])

            venta.recalcular_total()

        return JsonResponse({
            "mensaje": "Venta creada correctamente",
            "venta_id": venta.id,
            "total": venta.total
        }, status=201)

    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no existe"}, status=404)

    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no existe"}, status=404)

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




@csrf_exempt
def crear_cliente(request):
    if request.method == "POST":
        data = json.loads(request.body)

        cliente = Cliente.objects.create(
            numero_documento=data.get("numero_documento"),
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            fecha_nacimiento=data.get("fecha_nacimiento") or None,
            rut=data.get("rut"),
            email=data.get("email"),
            telefono=data.get("telefono"),
            direccion=data.get("direccion"),
            numero=data.get("numero"),
            comuna=data.get("comuna"),
            departamento=data.get("departamento"),
            informacion_adicional=data.get("informacion_adicional"),
        )

        return JsonResponse({
            "mensaje": "Cliente creado",
            "id": cliente.id
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)




def buscar_cliente_rut(request):
    try:
        rut = request.GET.get("rut")

        if not rut:
            return JsonResponse({"error": "Debe enviar un RUT"}, status=400)

        # 🔍 Buscar cliente
        cliente = Cliente.objects.filter(rut=rut).first()

        if not cliente:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)

        return JsonResponse({
            "id": cliente.id,
            "numero_documento": cliente.numero_documento,
            "nombre": cliente.nombre or "",
            "apellido": cliente.apellido or "",
            "rut": cliente.rut or "",
            "email": cliente.email or "",
            "telefono": cliente.telefono or "",
            "direccion": cliente.direccion or "",
            "numero": cliente.numero or "",
            "comuna": cliente.comuna or "",
            "departamento": cliente.departamento or "",
            "informacion_adicional": cliente.informacion_adicional or "",
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def guardar_suscriptor(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        marca = request.POST.get("marca", "").strip()
        modelo = request.POST.get("modelo", "").strip()

        if not email:
            return JsonResponse({
                "ok": False,
                "error": "Email requerido"
            }, status=400)

        Suscriptor.objects.create(
            email=email,
            nombre=nombre,
            marca=marca,
            modelo=modelo
        )

        return JsonResponse({"ok": True})

    return JsonResponse({
        "ok": False,
        "error": "Método no permitido"
    }, status=405)


def pagar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": producto.nombre,
                "quantity": 1,
                "unit_price": float(producto.precio),
                "currency_id": "CLP"
            }
        ],
        "back_urls": {
            "success": "https://zeezton.cl/pago-exitoso/",
            "failure": "https://zeezton.cl/pago-fallido/",
            "pending": "https://zeezton.cl/pago-pendiente/"
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    response = preference_response.get("response", {})

    if "init_point" not in response:
        return HttpResponse(f"Mercado Pago error: {preference_response}")

    return redirect(response["init_point"])

    from core.models import MovimientoInventario, DetalleMovimiento

def api_detalle_ventas(request):
    try:
        detalles = DetalleVenta.objects.select_related(
            "venta",
            "venta__cliente",
            "producto"
        ).all().order_by("-id")

        data = []

        for d in detalles:
            data.append({
                "id": d.id,
                "venta_id": d.venta.id,
                "fecha": d.venta.fecha.strftime("%d-%m-%Y %H:%M") if d.venta.fecha else "",
                "tipo_documento": d.venta.tipo_documento,
                "cliente": f"{d.venta.cliente.nombre} {d.venta.cliente.apellido}",
                "producto": d.producto.nombre,
                "cantidad": d.cantidad,
                "precio_unitario": int(d.precio_unitario),
                "subtotal": int(d.cantidad * d.precio_unitario),
                "total_venta": int(d.venta.total),
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)






@csrf_exempt
def crear_informe(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        titulo = data.get("titulo")
        descripcion = data.get("descripcion")
        tipo = data.get("tipo")
        prioridad = data.get("prioridad")
        estado = data.get("estado")

        if not titulo or not descripcion:
            return JsonResponse({"error": "Faltan datos"}, status=400)

        informe = Informe.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo,
            prioridad=prioridad,
            estado=estado
        )

        return JsonResponse({
            "mensaje": "Informe creado correctamente",
            "id": informe.id
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def listar_informes(request):
    try:
        informes = Informe.objects.all().order_by("-creado")

        data = []

        for i in informes:
            data.append({
                "id": i.id,
                "fecha": i.creado.strftime("%d-%m-%Y %H:%M") if i.creado else "",
                "tipo": i.tipo,
                "titulo": i.titulo,
                "prioridad": i.prioridad,
                "estado": i.estado,
                "descripcion": i.descripcion,
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def api_productos(request):
    try:
        productos = Producto.objects.select_related(
            "marca"
        ).order_by('-creado')

        data = []

        for p in productos:
            data.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.descripcion,
                "precio": int(p.precio),
                "stock": p.stock,
                "marca": p.marca.nombre if p.marca else "",
                "imagen": request.build_absolute_uri(p.imagen.url) if p.imagen else "",
                "destacado": p.destacado,
                "oferta": p.oferta,
                "super_oferta": p.super_oferta
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)