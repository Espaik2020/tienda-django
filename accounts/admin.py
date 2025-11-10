# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from .models import Profile

User = get_user_model()


# ==== Mixin reutilizable: columna "Acciones" (Editar / Eliminar) ====
class RowActionsMixin:
    """Agrega una columna 'Acciones' con enlaces a editar y eliminar."""
    def _admin_url(self, obj, action: str) -> str:
        opts = self.model._meta
        return reverse(f"admin:{opts.app_label}_{opts.model_name}_{action}", args=(obj.pk,))

    def acciones(self, obj):
        change_url = self._admin_url(obj, "change")
        delete_url = self._admin_url(obj, "delete")
        return format_html(
            '<a href="{}" class="button" style="margin-right:8px;">Editar</a>'
            '<a href="{}" class="button" style="color:#b91c1c;">Eliminar</a>',
            change_url, delete_url
        )
    acciones.short_description = "Acciones"


# ==== 1) Admin de Sesiones: quién, cuándo expira + Acciones ====
@admin.register(Session)
class SessionAdmin(RowActionsMixin, admin.ModelAdmin):
    list_display = ("user_link", "session_key", "expire_date", "estado", "acciones")
    list_filter = ("expire_date",)
    search_fields = ("session_key",)
    ordering = ("-expire_date",)

    def user_link(self, obj):
        data = obj.get_decoded()
        uid = data.get("_auth_user_id")
        if not uid:
            return "— anónima —"
        try:
            u = User.objects.get(pk=uid)
            # link a la ficha del usuario en el admin
            return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', u.pk, u.get_username())
        except User.DoesNotExist:
            return f"(id {uid})"
    user_link.short_description = "Usuario"

    def estado(self, obj):
        expired = obj.expire_date <= timezone.now()
        color = "#ef4444" if expired else "#16a34a"
        text = "Expirada" if expired else "Activa"
        return format_html(
            '<span style="padding:2px 8px;border-radius:12px;background:{};color:white;font-weight:600;">{}</span>',
            color, text
        )
    estado.short_description = "Estado"

    actions = ["eliminar_sesiones_expiradas"]

    def eliminar_sesiones_expiradas(self, request, queryset):
        count = Session.objects.filter(expire_date__lte=timezone.now()).delete()[0]
        self.message_user(request, f"Sesiones expiradas eliminadas: {count}")
    eliminar_sesiones_expiradas.short_description = "Eliminar TODAS las sesiones expiradas"


# ==== 2) Usuario: columna Nº de sesiones activas ====
class MyUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("active_sessions", "last_login",)
    ordering = ("-date_joined",)

    def active_sessions(self, obj):
        # Recorre sesiones no expiradas y cuenta cuántas pertenecen al usuario.
        now = timezone.now()
        total = 0
        for s in Session.objects.filter(expire_date__gt=now).only("session_key", "expire_date"):
            data = s.get_decoded()
            if data.get("_auth_user_id") == str(obj.pk):
                total += 1
        return total
    active_sessions.short_description = "Sesiones activas"


# Re-registrar el admin de User con nuestra clase
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, MyUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "avatar_preview")
    search_fields = ("user__username", "display_name", "user__email")
    list_select_related = ("user",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">', obj.avatar.url)
        return "—"
    avatar_preview.short_description = "Avatar"

    