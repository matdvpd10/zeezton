from django import forms
from django.forms import ModelForm
from .models import Producto, Reseña


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



class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ["nombre", "email", "calificacion", "comentario"]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "zf-input",
                "placeholder": "Tu nombre",
                "id": "id_nombre"
            }),
            "email": forms.EmailInput(attrs={
                "class": "zf-input",
                "placeholder": "Tu correo",
                "id": "id_email"
            }),
            "calificacion": forms.Select(attrs={
                "class": "zf-input",
                "id": "id_calificacion"
            }),
            "comentario": forms.Textarea(attrs={
                "class": "zf-input",
                "rows": 4,
                "placeholder": "Escribe tu reseña...",
                "id": "id_comentario"
            }),
        }