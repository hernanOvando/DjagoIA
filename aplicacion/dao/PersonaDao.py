from django.db import connection
from aplicacion.models.Persona import Persona


class PersonaDao:
    def crear(self, persona):
        sql = "INSERT INTO personas (nombre, email, password) VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (persona.nombre, persona.email, persona.password))
            persona.id = cursor.lastrowid
        return persona

    def listar_todos(self):
        sql = "SELECT idPersona, nombre, email FROM personas"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return [Persona(row[0], row[1], row[2]) for row in cursor.fetchall()]

    def obtener_por_id(self, id):
        sql = "SELECT idPersona, nombre, email, password FROM personas WHERE idPersona = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row:
                return Persona(row[0], row[1], row[2], row[3])
            return None

    def obtener_por_email(self, email):
        sql = "SELECT idPersona, nombre, email, password FROM personas WHERE email = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row:
                return Persona(row[0], row[1], row[2], row[3])
            return None

    def actualizar(self, persona):
        sql = "UPDATE personas SET nombre = %s, email = %s, password = %s WHERE idPersona = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (persona.nombre, persona.email, persona.password, persona.id))

    def eliminar(self, id):
        sql = "DELETE FROM personas WHERE idPersona = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (id,))
