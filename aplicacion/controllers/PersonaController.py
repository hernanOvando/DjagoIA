from django.contrib import messages
from aplicacion.services.PersonaService import PersonaService


class PersonaController:
    def __init__(self):
        self.service = PersonaService()

    def listar(self, request):
        persona_id = request.session.get("persona_id")
        persona = self.service.obtener_por_id(persona_id) if persona_id else None
        return [persona] if persona else []

    def crear(self, request):
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            password = request.POST.get("password", "")
            if nombre and email:
                persona = self.service.crear(nombre, email, password)
                request.session["persona_id"] = persona.id
                request.session["persona_nombre"] = persona.nombre
                messages.success(request, "Cuenta creada exitosamente.")
                return True
        return False

    def obtener_por_id(self, id):
        return self.service.obtener_por_id(id)

    def actualizar(self, request, id):
        persona = self.service.obtener_por_id(id)
        if not persona:
            messages.error(request, "Persona no encontrada.")
            return None
        if persona.id != request.session.get("persona_id"):
            messages.error(request, "No tienes permiso para editar esta cuenta.")
            return None
        if request.method == "POST":
            nombre = request.POST.get("nombre")
            email = request.POST.get("email")
            self.service.actualizar(id, nombre, email)
            request.session["persona_nombre"] = nombre
            messages.success(request, "Persona actualizada exitosamente.")
        return persona

    def eliminar(self, request, id):
        if request.method == "POST":
            persona = self.service.obtener_por_id(id)
            if persona and persona.id == request.session.get("persona_id"):
                self.service.eliminar(id)
                request.session.flush()
                messages.success(request, "Cuenta eliminada exitosamente.")
