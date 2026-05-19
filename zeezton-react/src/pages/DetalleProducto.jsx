{% extends 'core/base.html' %}
{% load static %}
{% load currency_filters %}

{% block title %}{{ producto.nombre }}{% endblock %}

{% block main_content %}
<div class="product-detail-mobile">

  <div class="product-gallery-box">
    {% if imagen_principal %}
      <img src="{{ imagen_principal.imagen.url }}" alt="{{ producto.nombre }}" class="product-main-image">
    {% elif producto.imagen %}
      <img src="{{ producto.imagen.url }}" alt="{{ producto.nombre }}" class="product-main-image">
    {% else %}
      <img src="{% static 'core/img/image_not_found.jpg' %}" alt="Sin imagen" class="product-main-image">
    {% endif %}
  </div>

  {% if imagenes %}
  <div class="product-thumbs">
    {% for img in imagenes %}
      {% if img.imagen %}
        <img src="{{ img.imagen.url }}" alt="{{ producto.nombre }}" class="product-thumb">
      {% endif %}
    {% endfor %}
  </div>
  {% endif %}

  <section class="product-info-premium">
    <span class="product-status">Disponible</span>

    <h1>{{ producto.nombre }}</h1>

    <p class="product-brand">
      Marca: <span>{{ producto.marca }}</span>
    </p>

    <div class="product-price">
      ${{ producto.precio|clp }} CLP
    </div>

    <div class="product-stock">
      Stock disponible: {{ producto.stock }}
    </div>

    <div class="product-benefits">
      <div>
        <i class="fa fa-shield"></i>
        <span>Calidad premium</span>
      </div>
      <div>
        <i class="fa fa-wrench"></i>
        <span>Fácil instalación</span>
      </div>
      <div>
        <i class="fa fa-star"></i>
        <span>Acabado elegante</span>
      </div>
      <div>
        <i class="fa fa-check-circle"></i>
        <span>Compra segura</span>
      </div>
    </div>

    <a href="{% url 'pagar_producto' producto.id %}" class="btn-buy-premium">
      <i class="fa fa-bolt"></i> Comprar ahora
    </a>

    <a href="{% url 'product' %}" class="btn-back-premium">
      <i class="fa fa-arrow-left"></i> Volver a productos
    </a>
  </section>

  <section class="product-description-premium">
    <h3>Descripción del producto</h3>

    <p>
      {% if producto.descripcion %}
        {{ producto.descripcion }}
      {% else %}
        Producto seleccionado especialmente para mejorar la estética, comodidad y personalización de tu vehículo.
      {% endif %}
    </p>
  </section>

</div>
{% endblock %}