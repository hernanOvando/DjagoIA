from django.shortcuts import render, redirect
from aplicacion.controllers.PersonaController import PersonaController
from aplicacion.controllers.NotaController import NotaController
from aplicacion.controllers.AuthController import AuthController

persona_controller = PersonaController()
nota_controller = NotaController()
auth_controller = AuthController()


def login(request):
    if request.session.get("persona_id"):
        return redirect("notas_listar")
    if auth_controller.login(request):
        return redirect("notas_listar")
    return render(request, "login.html")


def logout(request):
    auth_controller.logout(request)
    return redirect("login")


def listar(request):
    personas = persona_controller.listar()
    return render(request, "persona/persona_list.html", {"personas": personas})

def index(request):
    return render(request, "index.html")

def crear(request):
    if persona_controller.crear(request):
        return redirect("listar")
    return render(request, "persona/persona_form.html")


def editar(request, id):
    persona = persona_controller.actualizar(request, id)
    if persona is None:
        return redirect("listar")
    if request.method == "POST":
        return redirect("listar")
    return render(request, "persona/persona_form.html", {"persona": persona})


def eliminar(request, id):
    persona_controller.eliminar(request, id)
    return redirect("listar")


def notas_listar(request):
    persona_id = request.session.get("persona_id")
    if not persona_id:
        return redirect("login")
    notas = nota_controller.listar(request)
    return render(request, "nota/nota_list.html", {"notas": notas})


def notas_crear(request):
    if not request.session.get("persona_id"):
        return redirect("login")
    if nota_controller.crear(request):
        return redirect("notas_listar")
    return render(request, "nota/nota_form.html")


def notas_editar(request, id):
    if not request.session.get("persona_id"):
        return redirect("login")
    nota = nota_controller.actualizar(request, id)
    if nota is None:
        return redirect("notas_listar")
    if request.method == "POST":
        return redirect("notas_listar")
    return render(request, "nota/nota_form.html", {"nota": nota})


def notas_eliminar(request, id):
    if not request.session.get("persona_id"):
        return redirect("login")
    nota_controller.eliminar(request, id)
    return redirect("notas_listar")
