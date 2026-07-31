from django.contrib import messages
from django.contrib.auth.hashers import check_password
from aplicacion.services.PersonaService import PersonaService


class AuthController:
    def __init__(self):
        self.service = PersonaService()

    def login(self, request):
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            persona = self.service.obtener_por_email(email)
            if persona and check_password(password, persona.password):
                request.session["persona_id"] = persona.id
                request.session["persona_nombre"] = persona.nombre
                messages.success(request, f"Bienvenido {persona.nombre}.")
                return True
            messages.error(request, "Email o contraseña incorrectos.")
        return False

    def logout(self, request):
        request.session.flush()
        messages.success(request, "Sesión cerrada exitosamente.")
