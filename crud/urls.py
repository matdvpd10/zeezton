from django.urls import path
from . import views

urlpatterns = [

    # 🔥 API
path('api/productos/', views.api_productos, name='api_productos'),
path('api/ventas/', views.crear_venta, name='api_ventas'),
path('api/clientes/crear/', views.crear_cliente, name='api_clientes_crear'),
path('api/clientes/buscar/', views.buscar_cliente_rut, name='api_clientes_buscar'),
path('api/detalle-ventas/', views.api_detalle_ventas, name='api_detalle_ventas'),
# API informes
path('api/informes/', views.crear_informe, name='api_crear_informe'),
path('api/informes/listar/', views.listar_informes, name='api_listar_informes'),

    # 🌐 Web normal (frontend)
    path('', views.root),
    path('products/', views.products_list),
    path('products/<str:product_id>/', views.product_detail),
    path('pagar/<int:producto_id>/', views.pagar_producto, name='pagar_producto'),
]