"""
URL configuration for sitio_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.shortcuts import redirect
from . import views
from .views import api_productos, vender_producto

urlpatterns = [
    path('', lambda request: redirect('home')),  # 👈 redirige "/" a "/home/"
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),


    path('product/<int:pk>/', views.product_detail, name='detalle_producto'),
    path('offers/', views.offers, name='offers'),
    path("api/productos/<int:pk>/", views.api_producto_detalle, name="api_producto_detalle"),
    path("api/productos/", api_productos, name="api_productos"),
    path("api/vender/", vender_producto),

]
