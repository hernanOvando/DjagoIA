class Nota:
    def __init__(self, id=None, idPersona=None, mensaje="", fecha=None):
        self._id = id
        self._idPersona = idPersona
        self._mensaje = mensaje
        self._fecha = fecha

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def idPersona(self):
        return self._idPersona

    @idPersona.setter
    def idPersona(self, valor):
        self._idPersona = valor

    @property
    def mensaje(self):
        return self._mensaje

    @mensaje.setter
    def mensaje(self, valor):
        self._mensaje = valor

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor
