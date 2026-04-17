from django.shortcuts import render, redirect,reverse
from .models import *
from .forms import ProductoForm

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
