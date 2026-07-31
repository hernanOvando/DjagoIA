# App Django — Block de Notas

## Stack
- Django 6.0.7 + Django REST Framework 3.17.1
- Python 3.14.6
- Entorno virtual: `.venv\` (activar con `.venv\Scripts\Activate.ps1`)
- MySQL (`localhost:3306`, BBDD: `Kake`, usuario: `root`)
- Frontend clásico (Django Templates) + SPA (vanilla JS)
- Sin ORM: SQL puro con `connection.cursor()`

## Estructura
```
config/           # settings.py, urls.py (raíz)
aplicacion/       # Frontend clásico + lógica de negocio
  models/         # Clases Persona.py, Nota.py (POO plana)
  dao/            # PersonaDao.py, NotaDao.py (SQL directo)
  services/       # PersonaService.py, NotaService.py (lógica + hashing)
  controllers/    # PersonaController.py, NotaController.py, AuthController.py
  views.py        # Vistas clásicas basadas en funciones
  urls.py         # URLs del frontend clásico
  templates/      # Plantillas HTML
  static/css/     # Estilos CSS
api/              # API REST (DRF)
  serializers.py  # PersonaSerializer, NotaSerializer
  views.py        # APIViews: PersonaList, PersonaDetail, NotaList, NotaDetail, Login, Logout
  urls.py         # Rutas del API
frontend/         # SPA
  index.html      # Interfaz
  app.js          # Cliente fetch con CSRF
manage.py
```

## URLs
| Ruta | Descripción |
|---|---|
| `/` | Landing + CRUD personas |
| `/crear/`, `/editar/<id>/`, `/eliminar/<id>/` | CRUD personas |
| `/login/`, `/logout/` | Autenticación |
| `/notas/` y subrutas | CRUD notas |
| `/api/personas/` y `/api/personas/<id>/` | API personas |
| `/api/notas/` y `/api/notas/<id>/` | API notas |
| `/api/login/`, `/api/logout/`, `/api/csrf/` | API auth |
| `/app/` | SPA |

## Modelos (tablas MySQL)
- **personas**: idPersona (PK), nombre, email, password (hasheado con `make_password`)
- **notas**: idNota (PK), idPersona (FK), mensaje, fecha

## Autenticación
- Sesiones Django con clave `persona_id` en `request.session`
- Passwords con `django.contrib.auth.hashers`
- No usa User model de Django

## Dependencias principales
- django, djangorestframework, mysqlclient
