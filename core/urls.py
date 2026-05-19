from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("home")),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("product/", views.product, name="product"),
    path("product/<int:pk>/", views.product_detail, name="detalle_producto"),
    path("offers/", views.offers, name="offers"),
]