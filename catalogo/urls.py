from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='inicio'),
    path('productos/', views.ProductoLista.as_view(), name='producto_lista'),
    path('producto/<slug:slug>/', views.ProductoDetalle.as_view(), name='producto_detalle'),

    # Carrito
    path('carrito/', views.carrito_detalle, name='carrito_detalle'),
    path('carrito/agregar/<int:producto_id>/', views.carrito_agregar, name='carrito_agregar'),
    path('carrito/quitar/<int:producto_id>/', views.carrito_quitar, name='carrito_quitar'),
    path('carrito/checkout/', views.carrito_checkout, name='carrito_checkout'),


    # 🆕 Checkout y pedidos
    path('checkout/', views.checkout, name='checkout'),                     # 🆕
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),            # 🆕
    path('pedido/<int:order_id>/', views.pedido_detalle, name='pedido_detalle'),  # 🆕

    # Marcas / Temáticas
    path('marcas/', views.MarcasLista.as_view(), name='marcas_lista'),
    path('marcas/<slug:slug>/', views.MarcaDetalle.as_view(), name='marca_detalle'),
    path('estilos/<slug:slug>/', views.TematicaDetalle.as_view(), name='tematica_detalle'),

    # Newsletter
    path('suscribir/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('suscribir/confirmar/<str:token>/', views.newsletter_confirm, name='newsletter_confirm'),

    # Perfil
    path('mi-cuenta/', views.cuenta_perfil, name='cuenta_perfil'),
]


