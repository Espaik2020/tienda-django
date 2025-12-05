from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_api, name="login_api"),
    path("productos/", views.productos_api, name="productos_api"),
]
