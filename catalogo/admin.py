# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils import timezone 
from .models import (
    Categoria, Producto, Marca, Estudio, Tematica, ProductoImagen, Segmento,
    NewsletterSubscriber, Order,
)

# ======================
# MARCA
# ======================
class RowActionsMixin:
    """Columna 'Acciones' con Editar/Eliminar (estilo Jazzmin)."""
    def _admin_url(self, obj, action: str) -> str:
        opts = self.model._meta
        from django.urls import reverse
        return reverse(f"admin:{opts.app_label}_{opts.model_name}_{action}", args=(obj.pk,))

    def acciones(self, obj):
        change_url = self._admin_url(obj, "change")
        delete_url = self._admin_url(obj, "delete")
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary" style="margin-right:8px;">Editar</a>'
            '<a href="{}" class="btn btn-sm btn-outline-danger">Eliminar</a>',
            change_url, delete_url
        )
    acciones.short_description = "Acciones"


@admin.register(Marca)
class MarcaAdmin(RowActionsMixin, admin.ModelAdmin):
    list_display = ("nombre", "slug", "logo_thumb", "productos_count", "acciones")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("nombre",)
    list_per_page = 25

    # Formulario: campo de archivo + vista previa de lectura
    fields = ("nombre", "slug", "logo", "logo_preview")
    readonly_fields = ("logo_preview",)

    # Miniatura en el listado
    def logo_thumb(self, obj):
        logo = getattr(obj, "logo", None)
        if logo:
            return format_html(
                '<img src="{}" style="height:28px;border-radius:6px;object-fit:contain;'
                'background:#fff;padding:2px;border:1px solid #e5e7eb;" />',
                logo.url,
            )
        return "—"
    logo_thumb.short_description = "Logo"

    # Vista previa en el formulario
    def logo_preview(self, obj):
        logo = getattr(obj, "logo", None)
        if logo:
            return format_html(
                '<div style="margin-top:6px">'
                '<img src="{}" style="max-height:160px;object-fit:contain;'
                'border:1px solid #e5e7eb;padding:4px;background:#fff;border-radius:8px;" />'
                '</div>',
                logo.url,
            )
        return "—"
    logo_preview.short_description = "Vista previa"

    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = "Productos"


# ======================
# ESTUDIO
# ======================
@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "logo_preview", "productos_count")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("nombre",)
    list_per_page = 25

    def logo_preview(self, obj):
        if getattr(obj, "logo", None):
            return format_html('<img src="{}" style="height:28px;border-radius:4px;" />', obj.logo.url)
        return "—"
    logo_preview.short_description = "Logo"

    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = "Productos"


# ======================
# TEMÁTICA
# ======================
@admin.register(Tematica)
class TematicaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "icono_preview", "productos_count")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("nombre",)
    list_per_page = 25

    def icono_preview(self, obj):
        if getattr(obj, "icono", None):
            return format_html('<img src="{}" style="height:24px;border-radius:4px;" />', obj.icono.url)
        return "—"
    icono_preview.short_description = "Icono"

    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = "Productos"


# ======================
# CATEGORÍA
# ======================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "imagen_preview", "productos_count")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("nombre",)
    list_per_page = 25

    def imagen_preview(self, obj):
        img = getattr(obj, "imagen", None)
        if img:
            return format_html('<img src="{}" style="height:28px;border-radius:4px;" />', img.url)
        return "—"
    imagen_preview.short_description = "Imagen"

    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = "N.º de productos"


# ======================
# SEGMENTO (Hombres/Mujeres/Niños/Unisex)
# ======================
@admin.register(Segmento)
class SegmentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "icono_preview", "productos_count")
    search_fields = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("nombre",)
    list_per_page = 25

    def icono_preview(self, obj):
        if getattr(obj, "icono", None):
            return format_html('<img src="{}" style="height:24px;border-radius:4px;" />', obj.icono.url)
        return "—"
    icono_preview.short_description = "Icono"

    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = "Productos"


# ======================
# FILTRO PERSONALIZADO
# ======================
class DisponibleFilter(admin.SimpleListFilter):
    title = "Disponibilidad"
    parameter_name = "disponible"

    def lookups(self, request, model_admin):
        return (("si", "Disponible"), ("no", "No disponible"))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "si":
            return queryset.filter(activo=True, stock__gt=0)
        if value == "no":
            return queryset.exclude(activo=True, stock__gt=0)
        return queryset


# ======================
# INLINE: GALERÍA DE IMÁGENES
# ======================
class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ("preview", "imagen", "alt", "orden")
    readonly_fields = ("preview",)
    ordering = ("orden", "id")

    def preview(self, obj):
        if getattr(obj, "imagen", None):
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.imagen.url)
        return "—"
    preview.short_description = "Vista"


# ======================
# PRODUCTO
# ======================
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre", "categoria", "marca", "segmento",            # 👈 añadido segmento a tabla
        "precio", "descuento", "precio_final_admin",
        "stock", "activo", "destacado", "destacado_orden",
        "disponible_icono",
        "creado", "miniatura",
    )
    list_display_links = ("nombre",)
    list_filter = (
        "categoria", "marca", "estudio", "tematicas", "segmento",  # 👈 segmento en filtros
        "activo", "destacado",
        DisponibleFilter
    )
    search_fields = (
        "nombre", "slug", "categoria__nombre", "marca__nombre",
        "estudio__nombre", "tematicas__nombre", "segmento__nombre",  # 👈 buscable por segmento
        "descripcion"
    )
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("-destacado", "destacado_orden", "-creado")
    readonly_fields = ("creado", "preview", "precio_final_admin")
    list_per_page = 25
    list_editable = (
        "precio", "descuento", "stock", "activo",
        "destacado", "destacado_orden",
    )
    list_select_related = ("categoria", "marca", "estudio", "segmento")  # 👈 optimiza joins
    autocomplete_fields = ("marca", "estudio", "tematicas", "segmento")  # 👈 autocomplete segmento

    fieldsets = (
        ("Información básica", {"fields": ("nombre", "slug", "categoria", "descripcion")}),
        ("Taxonomías", {"fields": ("marca", "estudio", "tematicas", "segmento")}),  # 👈 añade segmento
        ("Precios", {"fields": ("precio", "descuento", "precio_final_admin")}),
        ("Inventario y estado", {"fields": ("stock", "activo")}),
        ("Imagen principal", {"fields": ("imagen", "preview")}),
        ("Destacados (home)", {"fields": ("destacado", "destacado_orden")}),
        ("Metadatos", {"fields": ("creado",)}),
    )

    inlines = [ProductoImagenInline]

    # --- Presentación ---
    def precio_final_admin(self, obj):
        final = obj.precio_final()
        return f"$ {final:,.2f}"
    precio_final_admin.short_description = "Precio final"

    def disponible_icono(self, obj):
        color = "#16a34a" if obj.disponible() else "#ef4444"
        texto = "Sí" if obj.disponible() else "No"
        return format_html(
            '<span style="padding:2px 8px;border-radius:12px;background:{};color:white;font-weight:600;">{}</span>',
            color, texto
        )
    disponible_icono.short_description = "Disponible"

    def miniatura(self, obj):
        url = getattr(obj, "portada_url", None)
        url = url() if callable(url) else None
        if url:
            return format_html('<img src="{}" style="height:45px;border-radius:6px;" />', url)
        return "—"
    miniatura.short_description = "Imagen"

    def preview(self, obj):
        url = getattr(obj, "portada_url", None)
        url = url() if callable(url) else None
        if url:
            return format_html('<img src="{}" style="max-height:220px;border-radius:10px;" />', url)
        return "Sin imagen"
    preview.short_description = "Previsualización"

    # --- Guardado ---
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.nombre)
        super().save_model(request, obj, form, change)

# NEWSLETTER (Suscriptores)
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_confirmed", "created_at", "confirmed_at", "token_short")
    search_fields = ("email", "token")
    list_filter = ("is_confirmed", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "confirmed_at", "token")
    actions = ["mark_confirmed"]

    def token_short(self, obj):
        return (obj.token[:10] + "…") if obj.token else "—"
    token_short.short_description = "Token"

    def save_model(self, request, obj, form, change):
        # genera token si no existe usando tu método del modelo
        if not obj.token and hasattr(obj, "ensure_token"):
            obj.ensure_token()
        super().save_model(request, obj, form, change)

    def mark_confirmed(self, request, queryset):
        updated = queryset.update(is_confirmed=True, confirmed_at=timezone.now())
        self.message_user(request, f"{updated} suscriptor(es) marcados como confirmados.")
    mark_confirmed.short_description = "Marcar como confirmados"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total", "status", "items_count")
    list_filter = ("status", "created_at")
    search_fields = ("id", "user__email", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "items_pretty")

    fieldsets = (
        ("Pedido", {"fields": ("user", "status", "total", "created_at")}),
        ("Contenido (snapshot JSON)", {"fields": ("items_pretty",)}),
    )

    def items_count(self, obj):
        try:
            return sum(int(i.get("qty", 1)) for i in (obj.items or []))
        except Exception:
            return 0
    items_count.short_description = "Artículos"

    def items_pretty(self, obj):
        import json
        return format_html(
            '<pre style="white-space:pre-wrap;margin:0">{}</pre>',
            json.dumps(obj.items or [], ensure_ascii=False, indent=2)
        )
    items_pretty.short_description = "Items (JSON)"



