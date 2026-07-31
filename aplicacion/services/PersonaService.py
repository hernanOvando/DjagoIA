from django.contrib.auth.hashers import make_password
from aplicacion.dao.PersonaDao import PersonaDao
from aplicacion.models.Persona import Persona


class PersonaService:
    def __init__(self):
        self.dao = PersonaDao()

    def crear(self, nombre, email, password=""):
        persona = Persona(nombre=nombre, email=email, password=make_password(password))
        return self.dao.crear(persona)
    
    def obtener_por_email(self, email):
        return self.dao.obtener_por_email(email)

    def listar_todos(self):
        return self.dao.listar_todos()

    def obtener_por_id(self, id):
        return self.dao.obtener_por_id(id)

    def actualizar(self, id, nombre, email, password=None):
        persona = self.dao.obtener_por_id(id)
        if persona:
            persona.nombre = nombre
            persona.email = email
            if password is not None:
                persona.password = make_password(password)
            self.dao.actualizar(persona)
        return persona

    def eliminar(self, id):
        self.dao.eliminar(id)
