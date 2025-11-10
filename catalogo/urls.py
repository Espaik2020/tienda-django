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

    # Marcas / Temáticas
    path('marcas/', views.MarcasLista.as_view(), name='marcas_lista'),
    path('marcas/<slug:slug>/', views.MarcaDetalle.as_view(), name='marca_detalle'),
    path('estilos/<slug:slug>/', views.TematicaDetalle.as_view(), name='tematica_detalle'),

    # Newsletter (nuevo)
    path('suscribir/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('suscribir/confirmar/<str:token>/', views.newsletter_confirm, name='newsletter_confirm'),

    # 💠 NUEVA RUTA PARA EL PERFIL DE USUARIO
    path('mi-cuenta/', views.cuenta_perfil, name='cuenta_perfil'),
]

