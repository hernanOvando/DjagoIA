from aplicacion.dao.NotaDao import NotaDao
from aplicacion.models.Nota import Nota


class NotaService:
    def __init__(self):
        self.dao = NotaDao()

    def crear(self, idPersona, mensaje):
        nota = Nota(idPersona=idPersona, mensaje=mensaje)
        return self.dao.crear(nota)

    def listar_por_persona(self, idPersona):
        return self.dao.listar_por_persona(idPersona)

    def obtener_por_id(self, id):
        return self.dao.obtener_por_id(id)

    def actualizar(self, id, mensaje):
        nota = self.dao.obtener_por_id(id)
        if nota:
            nota.mensaje = mensaje
            self.dao.actualizar(nota)
        return nota

    def eliminar(self, id):
        self.dao.eliminar(id)
