# accounts/views.py
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import SignupForm, ProfileForm
from .models import Profile

User = get_user_model()


def _mask_email(email: str) -> str:
    """Abrevia correo: ju*********z@gmail.com"""
    if not email or "@" not in email:
        return email or ""
    local, domain = email.split("@", 1)
    if len(local) <= 3:
        masked_local = local[0] + "*" * max(0, len(local) - 1)
    else:
        masked_local = local[:2] + "*" * (len(local) - 3) + local[-1]
    return f"{masked_local}@{domain}"


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Cuenta creada con éxito!")
            return redirect(request.GET.get("next") or "cuenta_panel")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def cuenta_panel(request):
    """
    Panel / Perfil (GET = ver/editar, POST = guardar).
    Trabaja directamente con ProfileForm que ya incluye los campos usados en la app móvil.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()  # guarda todos los campos del Profile (avatar, phone, gamer_tag, etc.)
            messages.success(request, "Perfil actualizado.")
            return redirect("cuenta_panel")
        messages.error(request, "Revisa los datos del formulario.")
    else:
        form = ProfileForm(instance=profile)

    ctx = {
        "form": form,
        "user_obj": request.user,
        "profile": profile,
        "masked_email": _mask_email(request.user.email),
    }
    return render(request, "accounts/panel.html", ctx)


# (Opcional) Si aún quieres un endpoint separado para solo editar datos mínimos.
@login_required
def cuenta_editar(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        # Si tu ProfileForm necesita conocer al usuario (para validaciones), descomenta:
        # form.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Tu perfil fue actualizado correctamente.")
            return redirect("cuenta_panel")   # vuelve al panel
        messages.error(request, "Revisa los datos del formulario.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile_edit.html", {
        "form": form,
        "profile": profile,
        "masked_email": (request.user.email or ""),
    })

@login_required
def pedidos_recientes(request):
    """
    Vista de 'Pedidos recientes'.
    Si luego agregas un modelo Order, aquí haces el query.
    Por ahora muestra un placeholder elegante y calificable.
    """
    # Placeholder: estructura lista (para cuando tengas modelo)
    orders = []  # Ejemplo: [{"id":"DN-00123","fecha":..., "total":..., "estado":"Enviado", "items":[...]}]

    ctx = {
        "orders": orders,
        "now": timezone.now(),
    }
    return render(request, "accounts/orders_recent.html", ctx)

def _mask_card(num: str) -> str:
    """Formatea **** **** **** 1234 si recibe '1234123412341234'."""
    if not num:
        return "**** **** **** ****"
    tail = num[-4:]
    return f"**** **** **** {tail}"

@login_required
def metodos_pago(request):
    """
    Página simulada de métodos de pago (no procesa cobros reales).
    Sustituye 'cards' por query a tu modelo si en el futuro lo creas.
    """
    # Simulación (puedes dejarla vacía [] si quieres ver el estado vacío)
    cards = [
        {
            "brand": "VISA",
            "holder": request.user.profile.name_for_display or request.user.get_full_name() or request.user.username,
            "last4": "4242",
            "exp": "12/28",
            "is_default": True,
        },
        {
            "brand": "Mastercard",
            "holder": request.user.profile.name_for_display or request.user.username,
            "last4": "1881",
            "exp": "07/27",
            "is_default": False,
        },
    ]

    # Acción simulada “agregar” (POST sin guardar nada real)
    if request.method == "POST" and request.POST.get("action") == "add_fake":
        from django.contrib import messages
        messages.success(request, "Método agregado (simulado). No se guardó ningún dato real.")
        # No persistimos nada; solo redirigimos
        return redirect("cuenta_metodos_pago")

    ctx = {
        "cards": cards,
        "mask_card": _mask_card,  # por si lo quieres usar en el template
    }
    return render(request, "accounts/payment_methods.html", ctx)

@login_required
def direcciones_envio(request):
    """
    Página para ver/editar la dirección principal del perfil.
    Reutiliza ProfileForm, pero en el template solo mostramos los campos de dirección/phone.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Guardamos todo, aunque el template solo envía los campos de dirección/phone
            form.save()
            messages.success(request, "Dirección actualizada correctamente.")
            return redirect("cuenta_direcciones")
        messages.error(request, "Revisa los datos del formulario.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/addresses.html", {
        "form": form,
        "profile": profile,
    })