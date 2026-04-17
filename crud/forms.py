from django import forms
from django.forms import ModelForm
from .models import Producto, Reseña   # 👈 importa también Reseña


class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'id',
            'descripcion',
            'marca',
            'precio',
            'stock',
            'imagen'
        ]
        labels = {
            'id': 'ID',
            'descripcion': 'Descripción',
            'marca': 'Marca',
            'precio': 'Precio Unitario',
            'stock': 'Stock',
            'imagen': 'Imagen'
        }
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'id': 'id'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'id': 'descripcion'}),
            'marca': forms.Select(attrs={'class': 'form-control', 'id': 'marca'}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'id': 'precio'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'id': 'stock'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'id': 'imagen'})
        }


# ✅ Nuevo formulario para reseñas
class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ["nombre", "email", "calificacion", "comentario"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Tu nombre"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Tu correo"}),
            "calificacion": forms.Select(attrs={"class": "form-select"}),
            "comentario": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Escribe tu reseña..."}),
        }
