class Persona:
    def __init__(self, id=None, nombre="", email="", password=""):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._password = password

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, valor):
        self._password = valor
