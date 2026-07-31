# Vistas de la API REST. Cada clase maneja un endpoint con métodos HTTP.
from django.contrib.auth.hashers import check_password
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from aplicacion.services.PersonaService import PersonaService
from aplicacion.services.NotaService import NotaService
from api.serializers import PersonaSerializer, NotaSerializer


class CSRFToken(APIView):
    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class PersonaList(APIView):
    # GET /api/personas/ - lista todas las personas
    def get(self, request):
        service = PersonaService()
        personas = service.listar_todos()
        serializer = PersonaSerializer(personas, many=True)
        return Response(serializer.data)

    # POST /api/personas/ - crea una nueva persona
    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonaDetail(APIView):
    # GET /api/personas/<id>/ - obtiene una persona por su ID
    def get(self, request, id):
        service = PersonaService()
        persona = service.obtener_por_id(id)
        if not persona:
            return Response({"error": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonaSerializer(persona)
        return Response(serializer.data)

    # PUT /api/personas/<id>/ - actualiza una persona existente
    def put(self, request, id):
        service = PersonaService()
        persona = service.obtener_por_id(id)
        if not persona:
            return Response({"error": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PersonaSerializer(persona, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/personas/<id>/ - elimina una persona
    def delete(self, request, id):
        service = PersonaService()
        persona = service.obtener_por_id(id)
        if not persona:
            return Response({"error": "Persona no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        service.eliminar(id)
        return Response({"mensaje": "Persona eliminada exitosamente"}, status=status.HTTP_200_OK)


class NotaList(APIView):
    # GET /api/notas/ - lista las notas de la persona autenticada
    def get(self, request):
        persona_id = request.session.get("persona_id")
        if not persona_id:
            return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        service = NotaService()
        notas = service.listar_por_persona(persona_id)
        serializer = NotaSerializer(notas, many=True)
        return Response(serializer.data)

    # POST /api/notas/ - crea una nueva nota (asociada a la sesión actual)
    def post(self, request):
        persona_id = request.session.get("persona_id")
        if not persona_id:
            return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data["idPersona"] = persona_id  # fuerza el ID de la sesión
        serializer = NotaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotaDetail(APIView):
    # GET /api/notas/<id>/ - obtiene una nota por su ID (solo si pertenece al usuario)
    def get(self, request, id):
        persona_id = request.session.get("persona_id")
        if not persona_id:
            return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        service = NotaService()
        nota = service.obtener_por_id(id)
        if not nota:
            return Response({"error": "Nota no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        if nota.idPersona != persona_id:
            return Response({"error": "No tienes permiso para ver esta nota"}, status=status.HTTP_403_FORBIDDEN)
        serializer = NotaSerializer(nota)
        return Response(serializer.data)

    # PUT /api/notas/<id>/ - actualiza una nota (solo si pertenece al usuario)
    def put(self, request, id):
        persona_id = request.session.get("persona_id")
        if not persona_id:
            return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        service = NotaService()
        nota = service.obtener_por_id(id)
        if not nota:
            return Response({"error": "Nota no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        if nota.idPersona != persona_id:
            return Response({"error": "No tienes permiso para editar esta nota"}, status=status.HTTP_403_FORBIDDEN)
        serializer = NotaSerializer(nota, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/notas/<id>/ - elimina una nota (solo si pertenece al usuario)
    def delete(self, request, id):
        persona_id = request.session.get("persona_id")
        if not persona_id:
            return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)
        service = NotaService()
        nota = service.obtener_por_id(id)
        if not nota:
            return Response({"error": "Nota no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        if nota.idPersona != persona_id:
            return Response({"error": "No tienes permiso para eliminar esta nota"}, status=status.HTTP_403_FORBIDDEN)
        service.eliminar(id)
        return Response({"mensaje": "Nota eliminada exitosamente"}, status=status.HTTP_200_OK)


class Login(APIView):
    # POST /api/login/ - inicia sesión con email y contraseña
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"error": "Email y contraseña requeridos"}, status=status.HTTP_400_BAD_REQUEST)
        service = PersonaService()
        persona = service.obtener_por_email(email)
        if persona and check_password(password, persona.password):
            request.session["persona_id"] = persona.id
            request.session["persona_nombre"] = persona.nombre
            return Response({
                "mensaje": f"Bienvenido {persona.nombre}",
                "id": persona.id,
                "nombre": persona.nombre,
                "email": persona.email,
            })
        return Response({"error": "Email o contraseña incorrectos"}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    # POST /api/logout/ - cierra la sesión actual
    def post(self, request):
        request.session.flush()
        return Response({"mensaje": "Sesión cerrada exitosamente"})
