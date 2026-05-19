from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('products/', views.products_list),
    path('products/<str:product_id>/', views.product_detail),
    path('pagar/<int:producto_id>/', views.pagar_producto, name='pagar_producto'),
]