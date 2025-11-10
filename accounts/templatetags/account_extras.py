# accounts/templatetags/account_extras.py
from django import template

register = template.Library()

@register.filter
def short_email(email: str) -> str:
    """
    Devuelve una versión corta del correo, p.ej. 'cesar.r…@g.mail'
    """
    if not email:
        return ""
    email = str(email)
    if "@" not in email:
        return email
    local, domain = email.split("@", 1)
    local_short = (local[:8] + "…") if len(local) > 9 else local
    parts = domain.split(".")
    if len(parts) == 1:
        domain_short = parts[0][:5]
    else:
        domain_short = f"{parts[0][:1]}.{parts[-1][:4]}"
    return f"{local_short}@{domain_short}"

@register.simple_tag
def avatar_url(user, default_url=""):
    """
    Retorna la URL del avatar del usuario si existe, si no el 'default_url'.
    Útil para:  <img src="{% avatar_url request.user static('img/default-avatar.png') %}">
    """
    try:
        avatar = getattr(user, "profile", None) and user.profile.avatar
        if avatar and hasattr(avatar, "url"):
            return avatar.url
    except Exception:
        pass
    return default_url
