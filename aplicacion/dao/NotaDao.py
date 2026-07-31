from django.db import connection
from aplicacion.models.Nota import Nota


class NotaDao:
    def crear(self, nota):
        sql = "INSERT INTO notas (idPersona, mensaje) VALUES (%s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (nota.idPersona, nota.mensaje))
            nota.id = cursor.lastrowid
        return nota

    def listar_por_persona(self, idPersona):
        sql = "SELECT idNota, idPersona, mensaje, fecha FROM notas WHERE idPersona = %s ORDER BY fecha DESC"
        with connection.cursor() as cursor:
            cursor.execute(sql, (idPersona,))
            return [Nota(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]

    def obtener_por_id(self, id):
        sql = "SELECT idNota, idPersona, mensaje, fecha FROM notas WHERE idNota = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row:
                return Nota(row[0], row[1], row[2], row[3])
            return None

    def actualizar(self, nota):
        sql = "UPDATE notas SET mensaje = %s WHERE idNota = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (nota.mensaje, nota.id))

    def eliminar(self, id):
        sql = "DELETE FROM notas WHERE idNota = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql, (id,))
