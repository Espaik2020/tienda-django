from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from catalogo.models import Producto      # ⚠️ confirma que tu modelo se llama Producto
from accounts.models import Profile       # ⚠️ si en accounts/models.py el modelo se llama distinto, cámbialo

User = get_user_model()


@csrf_exempt
def login_api(request):
    """
    POST /api/login/
    Campos: email, password
    Respuesta JSON para App Inventor.
    """
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Método no permitido"}, status=405)

    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()

    if not email or not password:
        return JsonResponse({"ok": False, "error": "Faltan datos"})

    # Buscamos por email (allauth ya usa email)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Usuario no encontrado"})

    if not user.check_password(password):
        return JsonResponse({"ok": False, "error": "Contraseña incorrecta"})

    profile = Profile.objects.filter(user=user).first()

    data_user = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "nombre": getattr(profile, "nombre", "") or user.get_username(),
    }

    return JsonResponse({"ok": True, "user": data_user})


def productos_api(request):
    """
    GET /api/productos/
    Devuelve catálogo simplificado para la app.
    """
    if request.method != "GET":
        return JsonResponse({"ok": False, "error": "Método no permitido"}, status=405)

    # ⚠️ Ajusta nombres de campos según catalogo/models.py
    qs = Producto.objects.all().values(
        "id",
        "nombre",       # por ejemplo: nombre, titulo, nombre_producto...
        "precio",       # por ejemplo: precio, precio_unitario...
        "imagen",       # por ejemplo: imagen, imagen_url, foto...
    )

    return JsonResponse({"ok": True, "productos": list(qs)})
