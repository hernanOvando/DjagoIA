from django.contrib import messages
from aplicacion.services.PersonaService import PersonaService


class PersonaController:
    def __init__(self):
        self.service = PersonaService()

    def listar(self):
        return self.service.listar_todos()

    def crear(self, request):
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            password = request.POST.get("password", "")
            if nombre and email:
                self.service.crear(nombre, email, password)
                messages.success(request, "Persona creada exitosamente.")
                return True
        return False

    def obtener_por_id(self, id):
        return self.service.obtener_por_id(id)

    def actualizar(self, request, id):
        persona = self.service.obtener_por_id(id)
        if not persona:
            messages.error(request, "Persona no encontrada.")
            return None
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            self.service.actualizar(id, nombre, email)
            messages.success(request, "Persona actualizada exitosamente.")
        return persona

    def eliminar(self, request, id):
        if request.method == "POST":
            self.service.eliminar(id)
            messages.success(request, "Persona eliminada exitosamente.")
