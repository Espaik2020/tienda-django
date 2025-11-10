# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, cuenta_panel, cuenta_editar, pedidos_recientes, metodos_pago, direcciones_envio   # ← importa cuenta_editar

urlpatterns = [
    # Panel y edición de perfil
    path("", cuenta_panel, name="cuenta_panel"),                 # /cuenta/
    path("editar/", cuenta_editar, name="cuenta_editar"),        # /cuenta/editar/
    path("pedidos/", pedidos_recientes, name="cuenta_pedidos"),
    path("metodos-pago/", metodos_pago, name="cuenta_metodos_pago"),
    path("direcciones/", direcciones_envio, name="cuenta_direcciones"), 

    # Auth: login / logout / registro
    path("ingresar/", auth_views.LoginView.as_view(
        template_name="accounts/login.html"), name="login"),
    path("salir/", auth_views.LogoutView.as_view(next_page="inicio"), name="logout"),
    path("registro/", signup, name="signup"),

    # Cambio de contraseña (lo que faltaba)
    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change_form.html"), name="password_change"),
    path("password-change/hecho/", auth_views.PasswordChangeDoneView.as_view(
        template_name="accounts/password_change_done.html"), name="password_change_done"),

    # Reset de contraseña (por email)
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"), name="password_reset"),
    path("password-reset/enviado/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset/completo/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]

