from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.urls import re_path
from django.views.static import serve as static_serve


urlpatterns = [
    path("admin/", admin.site.urls),

    # API para App Inventor
    path("api/", include("api.urls")),

    # Rutas de la tienda (home, productos, marcas, etc.)
    path("", include("catalogo.urls")),

    # Tu panel de cuenta (perfil/panel/editar propios)
    path("cuenta/", include("accounts.urls")),

    # Vistas de autenticación de ALLAUTH (login, signup, logout, password, etc.)
    # Montadas bajo /accounts/ (LOGIN_URL apunta a 'account_login')
    path("accounts/", include("allauth.urls")),

    # Atajo útil: /mi-cuenta/ -> redirige al panel de cuenta
    path("mi-cuenta/", RedirectView.as_view(pattern_name="cuenta_panel", permanent=False)),
]

# --------- Info / Ayuda / Políticas (páginas estáticas sencillas) ---------
urlpatterns += [
    path("info/como-comprar/",         TemplateView.as_view(template_name="info/como_comprar.html"),         name="como_comprar"),
    path("info/preguntas-frecuentes/", TemplateView.as_view(template_name="info/preguntas.html"),            name="preguntas_frecuentes"),
    path("info/pagos/",                TemplateView.as_view(template_name="info/pagos.html"),                name="pagos"),
    path("info/envio/",                TemplateView.as_view(template_name="info/envio.html"),                name="envio"),
    path("info/cambios-devoluciones/", TemplateView.as_view(template_name="info/cambios.html"),             name="cambios"),
    path("info/rastrea-tu-pedido/",    TemplateView.as_view(template_name="info/rastreo.html"),              name="rastreo"),
    path("info/facturacion/",          TemplateView.as_view(template_name="info/facturacion.html"),          name="facturacion"),

    path("empresa/quienes-somos/",     TemplateView.as_view(template_name="info/quienes.html"),              name="quienes_somos"),
    path("empresa/contacto/",          TemplateView.as_view(template_name="info/contacto.html"),             name="contacto"),
    path("empresa/proveedores/",       TemplateView.as_view(template_name="info/proveedores.html"),          name="proveedores"),
    path("empresa/ventas-corporativas/", TemplateView.as_view(template_name="info/ventas_corporativas.html"), name="ventas_corporativas"),
    path("empresa/sucursales/",        TemplateView.as_view(template_name="info/sucursales.html"),           name="sucursales"),
    path("empresa/empleo/",            TemplateView.as_view(template_name="info/empleo.html"),               name="empleo"),

    path("politicas/privacidad/",      TemplateView.as_view(template_name="info/privacidad.html"),           name="privacidad"),
    path("politicas/cookies/",         TemplateView.as_view(template_name="info/cookies.html"),              name="cookies"),
    path("politicas/compra/",          TemplateView.as_view(template_name="info/politica_compra.html"),      name="politica_compra"),
    path("politicas/terminos/",        TemplateView.as_view(template_name="info/terminos.html"),             name="terminos"),
    path("politicas/aviso-privacidad/", TemplateView.as_view(template_name="info/aviso_privacidad.html"),    name="aviso_privacidad"),
]

# --------- Alias cortos para login/signup/logout (opcional, útiles para enlaces sueltos) ---------
urlpatterns += [
    # /login  -> usa la vista "login" que definiste en accounts/urls.py
    path("login/",  RedirectView.as_view(pattern_name="login",  permanent=False)),

    # /signup -> usa tu vista signup de accounts/urls.py
    path("signup/", RedirectView.as_view(pattern_name="signup", permanent=False)),

    # /logout -> usa tu logout de accounts/urls.py
    path("logout/", RedirectView.as_view(pattern_name="logout", permanent=False)),
]

# Archivos estáticos y de medios en desarrollo
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Servir MEDIA también en hosting (opcional, activado por ENV)
if getattr(settings, "SERVE_MEDIA", False):
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
    ]
