from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

from crud.models import (
    Producto,
    Cliente,
    Venta,
    DetalleVenta,
    Informe,
    Suscriptor,
)


def obtener_imagen_producto(request, producto):
    imagen_extra = producto.imagenes.filter(
        principal=True
    ).order_by(
        "orden",
        "id"
    ).first()

    if not imagen_extra:
        imagen_extra = producto.imagenes.order_by(
            "orden",
            "id"
        ).first()

    if imagen_extra and imagen_extra.imagen:
        return request.build_absolute_uri(imagen_extra.imagen.url)

    if producto.imagen:
        return request.build_absolute_uri(producto.imagen.url)

    return ""


def api_productos(request):
    try:
        productos = Producto.objects.select_related(
            "marca"
        ).prefetch_related(
            "imagenes"
        ).order_by("-creado")

        data = []

        for p in productos:
            data.append({
                "id": p.id,
                "nombre": p.nombre,
                "descripcion": p.descripcion or "",
                "precio": int(p.precio),
                "stock": p.stock,
                "marca": p.marca.nombre if p.marca else "",
                "imagen": obtener_imagen_producto(request, p),
                "destacado": p.destacado,
                "oferta": p.oferta,
                "super_oferta": p.super_oferta,
                "calificacion": float(p.calificacion),
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def api_producto_detalle(request, pk):
    try:
        p = Producto.objects.select_related(
            "marca"
        ).prefetch_related(
            "imagenes"
        ).get(pk=pk)

        data = {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion or "",
            "precio": int(p.precio),
            "stock": p.stock,
            "marca": p.marca.nombre if p.marca else "",
            "imagen": obtener_imagen_producto(request, p),
            "destacado": p.destacado,
            "oferta": p.oferta,
            "super_oferta": p.super_oferta,
            "calificacion": float(p.calificacion),
            "imagenes": [
    {
        "id": img.id,
        "url": request.build_absolute_uri(img.imagen.url),
        "principal": img.principal,
        "orden": img.orden,
    }
    for img in p.imagenes.order_by("-principal", "orden", "id")
    if img.imagen
],
        }

        return JsonResponse(data, safe=False)

    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def crear_cliente(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
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
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def buscar_cliente_rut(request):
    try:
        rut = request.GET.get("rut")

        if not rut:
            return JsonResponse({"error": "Debe enviar un RUT"}, status=400)

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
                cantidad = int(item.get("cantidad", 0))

                if not producto_id or cantidad <= 0:
                    raise ValueError("Detalle inválido")

                producto = Producto.objects.select_for_update().get(id=producto_id)

                if producto.stock < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
                    )

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

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


def api_detalle_ventas(request):
    try:
        detalles = DetalleVenta.objects.select_related(
            "venta",
            "venta__cliente",
            "producto"
        ).order_by("-id")

        data = []

        for d in detalles:
            data.append({
                "id": d.id,
                "venta_id": d.venta.id,
                "fecha": d.venta.fecha.strftime("%d-%m-%Y %H:%M") if d.venta.fecha else "",
                "tipo_documento": d.venta.tipo_documento,
                "cliente": f"{d.venta.cliente.nombre or ''} {d.venta.cliente.apellido or ''}".strip(),
                "producto": d.producto.nombre,
                "cantidad": d.cantidad,
                "precio_unitario": int(d.precio_unitario),
                "subtotal": int(d.subtotal),
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


@csrf_exempt
def guardar_suscriptor(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        email = request.POST.get("email", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        marca = request.POST.get("marca", "").strip()
        modelo = request.POST.get("modelo", "").strip()

        if not email:
            return JsonResponse({"error": "Email requerido"}, status=400)

        Suscriptor.objects.create(
            email=email,
            nombre=nombre,
            marca=marca,
            modelo=modelo
        )

        return JsonResponse({"ok": True}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@csrf_exempt
def vender_producto(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)

        producto_id = data.get("producto_id")
        cantidad = int(data.get("cantidad", 0))

        if not producto_id or cantidad <= 0:
            return JsonResponse({"error": "Datos incompletos o cantidad inválida"}, status=400)

        producto = Producto.objects.select_for_update().get(id=producto_id)

        if producto.stock < cantidad:
            return JsonResponse({"error": "Stock insuficiente"}, status=400)

        producto.stock -= cantidad
        producto.save(update_fields=["stock"])

        return JsonResponse({
            "mensaje": "Venta realizada correctamente",
            "nuevo_stock": producto.stock
        })

    except Producto.DoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)