from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from aplicacion.services.PersonaService import PersonaService


def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuthController:
    LOGIN_MAX_ATTEMPTS = 10
    LOGIN_WINDOW = 60

    def __init__(self):
        self.service = PersonaService()

    def _login_bloqueado(self, ip):
        key = f"login_attempts:{ip}"
        return cache.get(key, 0) >= self.LOGIN_MAX_ATTEMPTS

    def _registrar_intento_fallido(self, ip):
        key = f"login_attempts:{ip}"
        attempts = cache.get(key, 0) + 1
        cache.set(key, attempts, self.LOGIN_WINDOW)

    def login(self, request):
        if request.method == "POST":
            ip = _get_client_ip(request)
            if self._login_bloqueado(ip):
                messages.error(request, "Demasiados intentos. Inténtalo más tarde.")
                return False
            email = request.POST.get("email")
            password = request.POST.get("password")
            persona = self.service.obtener_por_email(email)
            if persona and check_password(password, persona.password):
                request.session["persona_id"] = persona.id
                request.session["persona_nombre"] = persona.nombre
                messages.success(request, f"Bienvenido {persona.nombre}.")
                return True
            self._registrar_intento_fallido(ip)
            messages.error(request, "Email o contraseña incorrectos.")
        return False

    def logout(self, request):
        request.session.flush()
        messages.success(request, "Sesión cerrada exitosamente.")
