from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("shop/", views.product, name="product"),

    path(
        "producto/<int:pk>/",
        views.product_detail,
        name="detalle_producto"
    ),

    path("offers/", views.offers, name="offers"),

    path("about/", views.about, name="about"),

    path("contact/", views.contact, name="contact"),
]