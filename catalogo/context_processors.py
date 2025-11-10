# catalogo/context_processors.py
from django.db.models import Count, Q
from .models import Marca, Categoria, Tematica, Producto, Segmento  # 👈 añade Segmento

def menu_data(request):
    # criterio de "disponible"
    disponibles = Q(productos__activo=True, productos__stock__gt=0)

    # Marcas con productos disponibles
    marcas = (
        Marca.objects
        .annotate(num_prod=Count('productos', filter=disponibles))
        .filter(num_prod__gt=0)
        .order_by('nombre')
    )

    # Temáticas (estilos) con productos disponibles
    tematicas = (
        Tematica.objects
        .annotate(num_prod=Count('productos', filter=disponibles))
        .filter(num_prod__gt=0)
        .order_by('nombre')
    )

    # Categorías con productos disponibles
    categorias = (
        Categoria.objects
        .annotate(num_prod=Count('productos', filter=disponibles))
        .filter(num_prod__gt=0)
        .order_by('nombre')
    )

    # ✅ Segmentos con productos disponibles (para Hombres/Mujeres/Niños/Unisex)
    segmentos = (
        Segmento.objects
        .annotate(num_prod=Count('productos', filter=disponibles))
        .filter(num_prod__gt=0)
        .order_by('nombre')
    )

    # Contadores para el menú (badges)
    destacados_count = Producto.objects.filter(
        activo=True, stock__gt=0, destacado=True
    ).count()

    ofertas_count = Producto.objects.filter(
        activo=True, stock__gt=0, descuento__gt=0
    ).count()

    # (Opcional) cantidad total en carrito para badge
    cart = request.session.get("cart", {})
    cart_count = sum(int(q) for q in cart.values()) if cart else 0

    return {
        "marcas_menu": marcas,
        "tematicas_menu": tematicas,
        "categorias_menu": categorias,
        "segmentos_menu": segmentos,             # 👈 ahora disponible en templates
        "menu_destacados_count": destacados_count,
        "menu_ofertas_count": ofertas_count,
        "menu_cart_count": cart_count,           # 👈 úsalo en el botón Carrito
    }

