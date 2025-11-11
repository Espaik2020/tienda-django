# catalogo/views.py
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from .models import Producto, Categoria, Marca, Estudio, Tematica, Segmento  #  añade Segmento
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from .models import NewsletterSubscriber
from django.contrib.auth.decorators import login_required 
from .models import Order


# =======================
# HOME
# =======================
def home(request):
    # Destacados elegidos en admin (ordenados por destacado_orden)
    destacados = (Producto.objects
                  .filter(activo=True, stock__gt=0, destacado=True)
                  .select_related("categoria", "marca")
                  .order_by("destacado_orden", "-creado")[:8])

    # Nuevos
    nuevos = (Producto.objects
              .filter(activo=True, stock__gt=0)
              .select_related("categoria", "marca")
              .order_by("-creado")[:8])

    # Extras para el home
    categorias = Categoria.objects.order_by("nombre")[:8]
    marcas = Marca.objects.order_by("nombre")[:12]
    tematicas = (Tematica.objects
                 .annotate(num_prod=Count("productos", filter=Q(
                     productos__activo=True, productos__stock__gt=0
                 )))
                 .order_by("nombre")[:12])

    return render(request, "catalogo/home.html", {
        "destacados": destacados,
        "nuevos": nuevos,
        "categorias": categorias,
        "marcas": marcas,
        "tematicas": tematicas,
    })


# =======================
# LISTA DE PRODUCTOS + FILTROS
# =======================
class ProductoLista(ListView):
    model = Producto
    template_name = "catalogo/producto_lista.html"
    context_object_name = "productos"
    paginate_by = 12

    def get_queryset(self):
        qs = (Producto.objects
              .filter(activo=True, stock__gt=0)
              .select_related("categoria", "marca", "estudio", "segmento")  # 👈 optimiza
              .prefetch_related("tematicas")
              .order_by("-creado"))

        # filtros por querystring
        q = (self.request.GET.get("q") or "").strip()
        cat = (self.request.GET.get("cat") or "").strip()
        marca = (self.request.GET.get("marca") or "").strip()
        estudio = (self.request.GET.get("estudio") or "").strip()
        tematica = (self.request.GET.get("tematica") or "").strip()
        segmento = (self.request.GET.get("segmento") or "").strip()   # 👈 nuevo
        destacados = (self.request.GET.get("destacados") or "").strip()  # "1"
        ofertas = (self.request.GET.get("ofertas") or "").strip()        # "1"

        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(categoria__nombre__icontains=q) |
                Q(descripcion__icontains=q) |
                Q(marca__nombre__icontains=q) |
                Q(estudio__nombre__icontains=q) |
                Q(tematicas__nombre__icontains=q) |
                Q(segmento__nombre__icontains=q)   # 👈 busca por segmento
            )

        if cat:
            qs = qs.filter(
                Q(categoria__slug__iexact=cat) |
                Q(categoria__nombre__iexact=cat)
            )

        if marca:
            qs = qs.filter(
                Q(marca__slug__iexact=marca) |
                Q(marca__nombre__iexact=marca)
            )

        if estudio:
            qs = qs.filter(
                Q(estudio__slug__iexact=estudio) |
                Q(estudio__nombre__iexact=estudio)
            )

        if tematica:
            qs = qs.filter(
                Q(tematicas__slug__iexact=tematica) |
                Q(tematicas__nombre__iexact=tematica)
            )

        if segmento:
            qs = qs.filter(
                Q(segmento__slug__iexact=segmento) |
                Q(segmento__nombre__iexact=segmento)
            )

        if destacados in ("1", "true", "True"):
            qs = qs.filter(destacado=True).order_by("destacado_orden", "-creado")

        elif ofertas in ("1", "true", "True"):
            qs = qs.filter(descuento__gt=0).order_by("-descuento", "-creado")

        # Evita duplicados con M2M (temáticas)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.order_by("nombre")
        # conservar valores en el formulario/badges
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        ctx["cat"] = (self.request.GET.get("cat") or "").strip()
        ctx["marca_f"] = (self.request.GET.get("marca") or "").strip()
        ctx["estudio_f"] = (self.request.GET.get("estudio") or "").strip()
        ctx["tematica_f"] = (self.request.GET.get("tematica") or "").strip()
        ctx["segmento_f"] = (self.request.GET.get("segmento") or "").strip()     # 👈 nuevo
        ctx["destacados_f"] = (self.request.GET.get("destacados") or "").strip() # 👈 nuevo
        ctx["ofertas_f"] = (self.request.GET.get("ofertas") or "").strip()       # 👈 nuevo
        return ctx


# =======================
# DETALLE DE PRODUCTO
# =======================
class ProductoDetalle(DetailView):
    model = Producto
    template_name = "catalogo/producto_detalle.html"
    context_object_name = "producto"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (Producto.objects
                .filter(activo=True)
                .select_related("categoria", "marca", "estudio", "segmento")  # 👈 añade segmento
                .prefetch_related("tematicas", "imagenes"))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["galeria"] = self.object.imagenes.order_by("orden", "id")
        ctx["categorias"] = Categoria.objects.order_by("nombre")
        return ctx


# =======================
# MARCAS (LISTA Y DETALLE)
# =======================
class MarcasLista(ListView):
    model = Marca
    template_name = "catalogo/marcas_lista.html"
    context_object_name = "marcas"
    paginate_by = 24  # opcional

    def get_queryset(self):
        return (
            Marca.objects
            .annotate(
                num_prod=Count(
                    "productos",
                    filter=Q(productos__activo=True, productos__stock__gt=0)
                )
            )
            .order_by("nombre")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.order_by("nombre")
        ctx["productos_populares"] = (
            Producto.objects
            .filter(activo=True, stock__gt=0)
            .select_related("marca", "categoria", "estudio", "segmento")
            .prefetch_related("tematicas")
            .order_by("-destacado", "destacado_orden", "-creado")[:8]
        )
        # Alternativas:
        # .order_by("-creado")[:8]             # “Nuevos”
        # .filter(descuento__gt=0).order_by("-descuento", "-creado")[:8]  # “Ofertas”
        return ctx


class MarcaDetalle(ListView):
    model = Producto
    template_name = "catalogo/marca_detalle.html"
    context_object_name = "productos"
    paginate_by = 12

    def get_queryset(self):
        self.marca = get_object_or_404(Marca, slug=self.kwargs["slug"])
        self.estudio_slug = (self.request.GET.get("estudio") or "").strip()
        self.segmento_slug = (self.request.GET.get("segmento") or "").strip()  # 👈 opcional

        qs = (Producto.objects
              .filter(marca=self.marca, activo=True, stock__gt=0)
              .select_related("categoria", "marca", "estudio", "segmento")
              .prefetch_related("tematicas")
              .order_by("-creado"))

        if self.estudio_slug:
            qs = qs.filter(
                Q(estudio__slug__iexact=self.estudio_slug) |
                Q(estudio__nombre__iexact=self.estudio_slug)
            )

        if self.segmento_slug:
            qs = qs.filter(
                Q(segmento__slug__iexact=self.segmento_slug) |
                Q(segmento__nombre__iexact=self.segmento_slug)
            )

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        estudios = (Estudio.objects
                    .filter(productos__marca=self.marca,
                            productos__activo=True,
                            productos__stock__gt=0)
                    .distinct()
                    .annotate(num_prod=Count("productos", filter=Q(
                        productos__marca=self.marca,
                        productos__activo=True,
                        productos__stock__gt=0
                    ))))

        ctx["marca"] = self.marca
        ctx["estudios_marca"] = estudios
        ctx["estudio_f"] = self.estudio_slug
        ctx["segmento_f"] = self.segmento_slug  # 👈
        ctx["categorias"] = Categoria.objects.order_by("nombre")
        return ctx


# =======================
# TEMÁTICAS (DETALLE POR ESTILO)
# =======================
class TematicaDetalle(ListView):
    model = Producto
    template_name = "catalogo/tematica_detalle.html"
    context_object_name = "productos"
    paginate_by = 12

    def get_queryset(self):
        self.tematica = get_object_or_404(Tematica, slug=self.kwargs["slug"])
        self.marca_slug = (self.request.GET.get("marca") or "").strip()
        self.estudio_slug = (self.request.GET.get("estudio") or "").strip()
        self.segmento_slug = (self.request.GET.get("segmento") or "").strip()  # 👈 opcional

        qs = (Producto.objects
              .filter(tematicas=self.tematica, activo=True, stock__gt=0)
              .select_related("categoria", "marca", "estudio", "segmento")
              .prefetch_related("tematicas")
              .order_by("-creado"))

        if self.marca_slug:
            qs = qs.filter(Q(marca__slug__iexact=self.marca_slug) |
                           Q(marca__nombre__iexact=self.marca_slug))
        if self.estudio_slug:
            qs = qs.filter(Q(estudio__slug__iexact=self.estudio_slug) |
                           Q(estudio__nombre__iexact=self.estudio_slug))
        if self.segmento_slug:
            qs = qs.filter(Q(segmento__slug__iexact=self.segmento_slug) |
                           Q(segmento__nombre__iexact=self.segmento_slug))

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        marcas = (Marca.objects
                  .filter(productos__tematicas=self.tematica,
                          productos__activo=True,
                          productos__stock__gt=0)
                  .distinct()
                  .annotate(num_prod=Count("productos", filter=Q(
                      productos__tematicas=self.tematica,
                      productos__activo=True,
                      productos__stock__gt=0
                  ))))

        estudios = (Estudio.objects
                    .filter(productos__tematicas=self.tematica,
                            productos__activo=True,
                            productos__stock__gt=0)
                    .distinct()
                    .annotate(num_prod=Count("productos", filter=Q(
                        productos__tematicas=self.tematica,
                        productos__activo=True,
                        productos__stock__gt=0
                    ))))

        ctx["tematica"] = self.tematica
        ctx["marcas_tematica"] = marcas
        ctx["estudios_tematica"] = estudios
        ctx["marca_f"] = self.marca_slug
        ctx["estudio_f"] = self.estudio_slug
        ctx["segmento_f"] = self.segmento_slug  # 👈
        ctx["categorias"] = Categoria.objects.order_by("nombre")
        return ctx


# =======================
# CARRITO (SESIÓN)
# =======================
CART_SESSION_KEY = "cart"

def _get_cart(session):
    return session.get(CART_SESSION_KEY, {})

def _save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True

def carrito_detalle(request):
    cart = _get_cart(request.session)
    ids = [int(pid) for pid in cart.keys()]
    productos = Producto.objects.filter(id__in=ids)

    items = []
    subtotal = Decimal("0.00")
    descuento_total = Decimal("0.00")

    for p in productos:
        qty = int(cart.get(str(p.id), 0))
        # Precio base y final (si tienes precio_final())
        precio_base = Decimal(str(getattr(p, "precio", 0)))
        precio_unit = Decimal(str(p.precio_final() if hasattr(p, "precio_final") else p.precio))

        sub_base = (precio_base * qty).quantize(Decimal("0.01"))
        sub_unit = (precio_unit * qty).quantize(Decimal("0.01"))
        desc_linea = (sub_base - sub_unit).quantize(Decimal("0.01"))

        subtotal += sub_unit
        descuento_total += max(desc_linea, Decimal("0.00"))

        items.append({
            "producto": p,
            "cantidad": qty,
            "precio_unit": precio_unit,
            "precio_base": precio_base,
            "subtotal": sub_unit,
            "desc_linea": desc_linea,  # > 0 si hay oferta
        })

    envio_estimado = Decimal("50.00") if items else Decimal("0.00")
    total_con_envio = (subtotal + envio_estimado).quantize(Decimal("0.01"))

    return render(request, "catalogo/carrito.html", {
        "items": items,
        "subtotal": subtotal.quantize(Decimal("0.01")),
        "descuento_total": descuento_total.quantize(Decimal("0.01")),
        "envio_estimado": envio_estimado,
        "total_con_envio": total_con_envio,
        "total": subtotal.quantize(Decimal("0.01")),
        # Forzar móvil con ?m=1
        "force_mobile": (request.GET.get("m") == "1"),
        "categorias": Categoria.objects.order_by("nombre"),
    })

def carrito_agregar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id, activo=True)
    cart = _get_cart(request.session)
    qty = int((request.POST.get("qty") or request.GET.get("qty") or 1))
    actual = int(cart.get(str(producto_id), 0))
    nuevo = min(actual + qty, producto.stock)  # no exceder stock
    if nuevo > 0:
        cart[str(producto_id)] = nuevo
    _save_cart(request.session, cart)
    return redirect("carrito_detalle")

def carrito_quitar(request, producto_id):
    cart = _get_cart(request.session)
    remove_all = request.GET.get("all") == "1"
    if str(producto_id) in cart:
        if remove_all or cart[str(producto_id)] <= 1:
            cart.pop(str(producto_id))
        else:
            cart[str(producto_id)] = int(cart[str(producto_id)]) - 1
        _save_cart(request.session, cart)
    return redirect("carrito_detalle")

def _cart_items_and_total(session):
    """
    Convierte el carrito en:
      - items: lista de dicts [{id, name, price, qty}]
      - total: Decimal redondeado a 2 decimales
    Usa precio_final() si existe.
    """
    cart = _get_cart(session)  # dict: {product_id: qty}
    if not cart:
        return [], Decimal("0.00")

    ids = [int(pid) for pid in cart.keys()]
    productos = Producto.objects.filter(id__in=ids)

    items = []
    total = Decimal("0.00")

    for p in productos:
        qty = int(cart.get(str(p.id), 0))
        if qty <= 0:
            continue

        precio_unit = Decimal(str(p.precio_final() if hasattr(p, "precio_final") else p.precio)).quantize(Decimal("0.01"))
        subtotal = (precio_unit * qty).quantize(Decimal("0.01"))
        total += subtotal

        items.append({
            "id": p.id,
            "name": p.nombre,
            "price": float(precio_unit),  # JSON serializable
            "qty": qty,
        })

    return items, total.quantize(Decimal("0.01"))


def newsletter_subscribe(request):
    if request.method != "POST":
        return redirect("inicio")

    email = (request.POST.get("email") or "").strip().lower()
    if not email:
        messages.error(request, "Escribe tu correo para suscribirte.")
        return redirect(request.META.get("HTTP_REFERER") or "inicio")

    sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
    # Siempre forzamos token y marcamos como no confirmado
    sub.is_confirmed = False
    if not sub.token:
        import secrets
        sub.token = secrets.token_urlsafe(32)
    sub.save()

    # Link de confirmación absoluto
    confirm_url = request.build_absolute_uri(
        reverse("newsletter_confirm", args=[sub.token])
    )

    # Email (en desarrollo se imprime en consola por tu EMAIL_BACKEND)
    subject = "Confirma tu suscripción"
    body = (
        "¡Gracias por suscribirte a DNM Wear!\n\n"
        "Haz clic para confirmar tu correo:\n"
        f"{confirm_url}\n\n"
        "Si no fuiste tú, ignora este mensaje."
    )
    send_mail(subject, body, None, [email], fail_silently=True)

    messages.success(
        request,
        "Te enviamos un correo para confirmar tu suscripción. Revisa tu bandeja."
    )
    return redirect(request.META.get("HTTP_REFERER") or "inicio")


def newsletter_confirm(request, token):
    sub = NewsletterSubscriber.objects.filter(token=token).first()
    if not sub:
        messages.error(request, "Token inválido o vencido.")
        return redirect("inicio")

    sub.is_confirmed = True
    sub.confirmed_at = timezone.now()
    # Si quieres invalidar el token tras confirmar, descomenta:
    # sub.token = None
    sub.save()

    messages.success(request, "¡Suscripción confirmada! Gracias 😊")
    return redirect("inicio")

@login_required
def cuenta_perfil(request):
    # Envía a /cuenta/ (accounts.views.cuenta_panel)
    return redirect("cuenta_panel")

@login_required
def checkout(request):
    items, total = _cart_items_and_total(request.session)
    if not items:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("carrito_detalle")

    # Guarda pedido SIMULADO
    order = Order.objects.create(
        user=request.user,
        total=total,
        items=items,
        status="PAID",  # simulamos pago aprobado
    )

    # Limpia carrito
    _save_cart(request.session, {})

    messages.success(request, f"Compra simulada creada: Pedido #{order.id}")
    return redirect("pedido_detalle", order_id=order.id)


@login_required
def mis_pedidos(request):
    pedidos = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "catalogo/mis_pedidos.html", {"pedidos": pedidos})


@login_required
def pedido_detalle(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, user=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Pedido no encontrado.")
        return redirect("mis_pedidos")
    return render(request, "catalogo/pedido_detalle.html", {"order": order})
