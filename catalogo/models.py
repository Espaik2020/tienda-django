from decimal import Decimal
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.conf import settings
import secrets


# ========= MARCA =========
class Marca(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to="marcas/", blank=True, null=True)
    descripcion = RichTextField(blank=True, null=True)
    sitio_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("marca_detalle", args=[self.slug])


# ========= ESTUDIO =========
class Estudio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = RichTextField(blank=True, null=True)
    sitio_url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="estudios/", blank=True, null=True)
    banner = models.ImageField(upload_to="estudios/banners/", blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Estudio"
        verbose_name_plural = "Estudios"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("estudio_detalle", args=[self.slug])


# ========= TEMÁTICA =========
class Tematica(models.Model):
    """
    Para tipos/estilos/temas: 'indie', 'retro', 'pixel art', 'souls-like', etc.
    """
    nombre = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True)
    icono = models.ImageField(upload_to="tematicas/iconos/", blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Temática"
        verbose_name_plural = "Temáticas"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("tematica_detalle", args=[self.slug])
    
    def icono_safe_url(self):
        """Devuelve la URL del icono o None si no hay archivo físico."""
        if not self.icono:
            return None
        try:
            return self.icono.url
        except (ValueError, FileNotFoundError):
            return None


# ========= CATEGORÍA =========
class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = RichTextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="categorias/", blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# ========= NUEVO: SEGMENTO (Hombres/Mujeres/Niños/Unisex) =========
class Segmento(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True)
    icono = models.ImageField(upload_to="segmentos/iconos/", blank=True, null=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Segmento"
        verbose_name_plural = "Segmentos"

    def __str__(self):
        return self.nombre


# ========= PRODUCTO =========
class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("0.00"),
        help_text="Porcentaje de descuento (ej. 10.00 = 10%)"
    )
    descripcion = RichTextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # principal
    stock = models.PositiveIntegerField(default=0)

    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name='productos'
    )

    # ========= TAXONOMÍAS =========
    marca = models.ForeignKey(
        Marca, on_delete=models.PROTECT, related_name="productos",
        null=True, blank=True, help_text="Xbox, PlayStation, Nintendo, etc."
    )
    estudio = models.ForeignKey(
        Estudio, on_delete=models.PROTECT, related_name="productos",
        null=True, blank=True, help_text="Studio/Developer (opcional)"
    )
    tematicas = models.ManyToManyField(
        Tematica, related_name="productos", blank=True,
        help_text="Indie, Retro, Pixel Art, etc."
    )
    segmento = models.ForeignKey(
        Segmento, on_delete=models.SET_NULL, null=True, blank=True, related_name="productos",
        help_text="Hombres, Mujeres, Niños, Unisex"
    )
    # ==============================

    # Control del Home
    destacado = models.BooleanField(
        default=False,
        help_text="Aparece en la sección Destacados del home"
    )
    destacado_orden = models.PositiveIntegerField(
        default=0,
        help_text="Orden en el home (1 arriba)"
    )

    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("producto_detalle", args=[self.slug])

    def precio_final(self):
        """Devuelve el precio con descuento, redondeado a 2 decimales."""
        if self.descuento and self.descuento > 0:
            factor = (Decimal("1.00") - (self.descuento / Decimal("100")))
            return (self.precio * factor).quantize(Decimal("0.01"))
        return self.precio.quantize(Decimal("0.01"))

    def disponible(self):
        return self.stock > 0 and self.activo

    # Helpers para portada / URL
    def portada(self):
        if self.imagen:
            return self.imagen
        first = self.imagenes.first()
        return first.imagen if first else None

    def portada_url(self):
        img = self.portada()
        return img.url if img else None


# ========= GALERÍA DE IMÁGENES =========
class ProductoImagen(models.Model):
    producto = models.ForeignKey("Producto", on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos/galeria/")
    alt = models.CharField(max_length=120, blank=True)
    orden = models.PositiveIntegerField(default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "id"]
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de producto"

    def __str__(self):
        return f"Imagen de {self.producto.nombre} ({self.id})"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(max_length=191, unique=True)
    is_confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores"

    def __str__(self):
        return self.email

    def ensure_token(self):
        if not self.token:
            self.token = secrets.token_urlsafe(32)


# ========= PEDIDO (simulado) =========
class Order(models.Model):
    STATUS_CHOICES = [
        ("CREATED", "Creado"),
        ("PAID", "Pagado (simulado)"),
        ("CANCELLED", "Cancelado"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # total y snapshot de items (carrito) para demo
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    items = models.JSONField(default=list)  # [{"id":"SKU1","name":"...","price":199.0,"qty":2}, ...]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CREATED")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        who = self.user.email if (self.user and self.user.email) else "anónimo"
        return f"Pedido #{self.pk} - {who} - ${self.total}"
