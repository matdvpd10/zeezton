from django.urls import path
from . import views

urlpatterns = [

    path('productos/', views.api_productos),
    path('productos/<int:pk>/', views.api_producto_detalle),

    path('vender/', views.vender_producto),

    path('ventas/', views.crear_venta),

    path('clientes/crear/', views.crear_cliente),
    path('clientes/buscar/', views.buscar_cliente_rut),

    path('detalle-ventas/', views.api_detalle_ventas),

    path('informes/', views.crear_informe),
    path('informes/listar/', views.listar_informes),

]