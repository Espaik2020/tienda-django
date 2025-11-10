"""
Django settings for tienda project.
"""

from pathlib import Path
from django.contrib.messages import constants as messages  # para mapear a clases Bootstrap
import os
ENV = os.getenv

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

# === Seguridad / Debug ===
SECRET_KEY = 'django-insecure-8flvapccliex1a$!k1#tw1)fmu^ej51#=u&ng%2w_odiue6a-a'
DEBUG = True  # en prod se sobreescribe con DJ_DEBUG=false

# ⬇️ IMPORTANTE para probar desde el teléfono (red local)
ALLOWED_HOSTS = [
    "192.168.110.71",
    "127.0.0.1",
    "localhost",
    # ".ngrok-free.app",
]

# Para formularios/POST desde el teléfono (evita errores CSRF)
CSRF_TRUSTED_ORIGINS = [
    "http://192.168.110.71",
    "http://192.168.110.71:8000",
    # "https://*.ngrok-free.app",
]

# === Apps instaladas ===
INSTALLED_APPS = [
    # --- Admin con tema moderno ---
    "jazzmin",

    # --- Core Django ---
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # REQUERIDO por allauth
    "django.contrib.sites",

    # --- Editor de texto enriquecido ---
    "ckeditor",

    # --- Allauth (login/registro por email) ---
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # opcional

    # --- Tus apps ---
    "catalogo",
    "accounts",
]

# === Middleware ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Requerido por django-allauth
    "allauth.account.middleware.AccountMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tienda.urls"

# === Templates ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "catalogo.context_processors.menu_data",
            ],
        },
    },
]

WSGI_APPLICATION = "tienda.wsgi.application"

# === Base de datos (MySQL via WAMP/XAMPP) ===
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "tienda_db",
        "USER": "tienda_user",
        "PASSWORD": "TuPassSegura123!",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            # Ajuste para evitar el límite de índice en MySQL viejos
            "charset": "utf8",
            "collation": "utf8_general_ci",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# === Password validators ===
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# === Internacionalización ===
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Monterrey"
USE_I18N = True
USE_TZ = True

# === Archivos estáticos / media ===
STATIC_URL = "/static/"
# ✅ Deja aquí solo carpetas "globales" (si las tienes). NO metas 'catalogo/static'.
STATICFILES_DIRS = [
    BASE_DIR / "static",   # si no existe, puedes borrar esta línea
]
STATIC_ROOT = BASE_DIR / "staticfiles"

]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# === Llaves primarias por defecto ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# === Auth / Redirecciones (Allauth) ===
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "account_login"

# Política de cuentas (allauth) — nueva sintaxis (evita deprecados)
ACCOUNT_LOGIN_METHODS = {"email"}                              # reemplaza ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"] # reemplaza EMAIL_REQUIRED/USERNAME_REQUIRED
ACCOUNT_EMAIL_VERIFICATION = "mandatory"                       # exige verificación por correo

# === Email real (por defecto: consola en dev para no fallar mientras configuras SMTP) ===
# Cuando ya tengas SMTP, cambia a smtp y rellena variables (abajo hay override por ENV).
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "tu_cuenta@gmail.com"
EMAIL_HOST_PASSWORD = "tu_app_password_16chars"
DEFAULT_FROM_EMAIL = "Tienda <tu_cuenta@gmail.com>"

# === Mapear mensajes Django a clases Bootstrap ===
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# ---------- Jazzmin ----------
JAZZMIN_SETTINGS = {
    "site_title": "Tienda Gamer Admin",
    "site_header": "Tienda Gamer",
    "site_brand": "Panel de Catálogo",
    "welcome_sign": "Bienvenido al Panel",
}

# ---------- CKEditor ----------
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 200,
        "width": "100%",
    }
}

# =======================
#  Bloque de PRODUCCIÓN
#  (override por variables de entorno, sin romper tu dev)
# =======================

# DEBUG / SECRET_KEY por ENV
DEBUG = ENV("DJ_DEBUG", str(DEBUG)).lower() == "true"
SECRET_KEY = ENV("DJ_SECRET_KEY", SECRET_KEY)

# Hosts y CSRF por ENV (útil cuando subas a hosting/domino)
_env_hosts = ENV("DJ_ALLOWED_HOSTS")
if _env_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _env_hosts.split(",") if h.strip()]

_env_csrf = ENV("DJ_CSRF_ORIGINS")
if _env_csrf:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _env_csrf.split(",") if o.strip()]

# DB de producción opcional por ENV (si tu hosting te da otras credenciales)
if ENV("DJ_DB_NAME"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": ENV("DJ_DB_NAME"),
        "USER": ENV("DJ_DB_USER"),
        "PASSWORD": ENV("DJ_DB_PASSWORD"),
        "HOST": ENV("DJ_DB_HOST", "127.0.0.1"),
        "PORT": ENV("DJ_DB_PORT", "3306"),
        "OPTIONS": {
            "charset": "utf8",
            "collation": "utf8_general_ci",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }

if ENV("DATABASE_URL"):
    import dj_database_url
    DATABASES["default"] = dj_database_url.config(
        default=ENV("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )

# Email por ENV (puedes activar SMTP real sin tocar el código)
EMAIL_BACKEND = ENV("DJ_EMAIL_BACKEND", EMAIL_BACKEND)
EMAIL_HOST = ENV("DJ_EMAIL_HOST", EMAIL_HOST)
EMAIL_PORT = int(ENV("DJ_EMAIL_PORT", EMAIL_PORT))
EMAIL_USE_TLS = ENV("DJ_EMAIL_USE_TLS", "true").lower() == "true"
EMAIL_HOST_USER = ENV("DJ_EMAIL_USER", EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = ENV("DJ_EMAIL_PASS", EMAIL_HOST_PASSWORD)
DEFAULT_FROM_EMAIL = ENV("DJ_DEFAULT_FROM", DEFAULT_FROM_EMAIL)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# WhiteNoise solo cuando no estás en DEBUG (hosting simple sin Nginx)
if not DEBUG:
    # Añade soporte de staticfiles sin cambiar tu estructura
    if "whitenoise.runserver_nostatic" not in INSTALLED_APPS:
        INSTALLED_APPS = ["whitenoise.runserver_nostatic", *INSTALLED_APPS]
    if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
        # Garantiza SecurityMiddleware primero
        MIDDLEWARE = [
            "django.middleware.security.SecurityMiddleware",
            "whitenoise.middleware.WhiteNoiseMiddleware",
            *[mw for mw in MIDDLEWARE if mw not in (
                "django.middleware.security.SecurityMiddleware",
                "whitenoise.middleware.WhiteNoiseMiddleware",
            )],
        ]
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # Seguridad básica (activa HSTS cuando tengas HTTPS estable)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    
# === Override definitivo por DATABASE_URL (Postgres en Render) ===
import os as _os
_dburl = _os.environ.get("DATABASE_URL")
if _dburl:
    import dj_database_url as _dj
    # Fuerza a tomar la URL exacta que hay en el entorno
    DATABASES["default"] = _dj.parse(_dburl, conn_max_age=600, ssl_require=True)
