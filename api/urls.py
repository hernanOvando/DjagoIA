# Mapeo de URLs a las vistas de la API REST
from django.urls import path
from api import views

urlpatterns = [
    # CSRF Token
    path("csrf/", views.CSRFToken.as_view(), name="api_csrf"),
    # Personas
    path("personas/", views.PersonaList.as_view(), name="api_personas_list"),
    path("personas/<int:id>/", views.PersonaDetail.as_view(), name="api_personas_detail"),
    # Notas
    path("notas/", views.NotaList.as_view(), name="api_notas_list"),
    path("notas/<int:id>/", views.NotaDetail.as_view(), name="api_notas_detail"),
    # Autenticación
    path("login/", views.Login.as_view(), name="api_login"),
    path("logout/", views.Logout.as_view(), name="api_logout"),
]
