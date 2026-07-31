from django.contrib import messages
from aplicacion.services.NotaService import NotaService


class NotaController:
    def __init__(self):
        self.service = NotaService()

    def listar(self, request):
        persona_id = request.session.get("persona_id")
        if not persona_id:
            return []
        return self.service.listar_por_persona(persona_id)

    def crear(self, request):
        if request.method == "POST":
            persona_id = request.session.get("persona_id")
            mensaje = request.POST.get("mensaje")
            if persona_id and mensaje:
                self.service.crear(persona_id, mensaje)
                messages.success(request, "Nota creada exitosamente.")
                return True
        return False

    def obtener_por_id(self, id):
        return self.service.obtener_por_id(id)

    def actualizar(self, request, id):
        nota = self.service.obtener_por_id(id)
        if not nota:
            messages.error(request, "Nota no encontrada.")
            return None
        persona_id = request.session.get("persona_id")
        if nota.idPersona != persona_id:
            messages.error(request, "No tienes permiso para editar esta nota.")
            return None
        if request.method == "POST":
            mensaje = request.POST.get("mensaje")
            self.service.actualizar(id, mensaje)
            messages.success(request, "Nota actualizada exitosamente.")
        return nota

    def eliminar(self, request, id):
        if request.method == "POST":
            nota = self.service.obtener_por_id(id)
            if nota and nota.idPersona == request.session.get("persona_id"):
                self.service.eliminar(id)
                messages.success(request, "Nota eliminada exitosamente.")
