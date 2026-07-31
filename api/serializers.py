# Serializadores para convertir objetos Persona y Nota a JSON y viceversa
from rest_framework import serializers
from aplicacion.services.PersonaService import PersonaService
from aplicacion.services.NotaService import NotaService


class PersonaSerializer(serializers.Serializer):
    # Define los campos que se exponen en la API
    id = serializers.IntegerField(read_only=True)  # Solo lectura, lo asigna la BD
    nombre = serializers.CharField()                # Obligatorio
    email = serializers.EmailField()                # Validado como email
    password = serializers.CharField(write_only=True, required=False)  # Solo escritura, nunca se devuelve

    def create(self, validated_data):
        # Crea una nueva persona usando el servicio correspondiente
        service = PersonaService()
        persona = service.crear(
            validated_data.get("nombre"),
            validated_data.get("email"),
            validated_data.get("password", ""),
        )
        return persona

    def update(self, instance, validated_data):
        # Actualiza una persona existente
        service = PersonaService()
        persona = service.actualizar(
            instance.id,
            validated_data.get("nombre", instance.nombre),
            validated_data.get("email", instance.email),
            validated_data.get("password"),
        )
        return persona


class NotaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    idPersona = serializers.IntegerField()  # ID de la persona a la que pertenece
    mensaje = serializers.CharField()
    fecha = serializers.DateTimeField(read_only=True)  # La asigna la BD con NOW()

    def create(self, validated_data):
        service = NotaService()
        nota = service.crear(
            validated_data.get("idPersona"),
            validated_data.get("mensaje"),
        )
        return nota

    def update(self, instance, validated_data):
        service = NotaService()
        nota = service.actualizar(
            instance.id,
            validated_data.get("mensaje", instance.mensaje),
        )
        return nota
