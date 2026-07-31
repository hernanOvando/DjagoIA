from django.urls import path
from aplicacion import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listar/", views.listar, name="listar"),
    path("crear/", views.crear, name="crear"),
    path("editar/<int:id>/", views.editar, name="editar"),
    path("eliminar/<int:id>/", views.eliminar, name="eliminar"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("notas/", views.notas_listar, name="notas_listar"),
    path("notas/crear/", views.notas_crear, name="notas_crear"),
    path("notas/editar/<int:id>/", views.notas_editar, name="notas_editar"),
    path("notas/eliminar/<int:id>/", views.notas_eliminar, name="notas_eliminar"),
]
