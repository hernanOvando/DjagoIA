# App Django — Block de Notas

## Stack
- Django 6.0.7 + Django REST Framework 3.17.1 + mysqlclient + python-dotenv
- Python 3.14.6
- Entorno virtual: `.venv\` (activar con `.venv\Scripts\Activate.ps1`)
- MySQL + Frontend clásico (Django Templates) + SPA (vanilla JS)
- Sin ORM: SQL puro con `connection.cursor()` (DAO)

## Configuración
- Todo se lee de `.env` vía `python-dotenv` en `config/settings.py`: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SECRET_KEY`, `DEBUG`.
- Copiar `.env.example` → `.env` (defaults: `Kake` / `root` / `localhost:3306`). `.env` está en `.gitignore`; no se commitear.

## Gotchas
- **No hay migraciones**: `aplicacion/migrations/` y `api/migrations/` están vacíos. Las tablas `personas` y `notas` se crean a mano en MySQL; `manage.py migrate` no las crea.
- Los serializers son `serializers.Serializer` (no `ModelSerializer`): `create()`/`update()` llaman a `PersonaService`/`NotaService`, que escriben con SQL crudo.
- La SPA no usa un static server: `config/urls.py` monta `/app/` y `/app/<path:path>` con la view `frontend()` que sirve `frontend/` con `FileResponse`.
- Sesión: claves `persona_id` y `persona_nombre` en `request.session`. Auth vía `make_password`/`check_password` (django hashers), nunca en claro.
- Los tests (`aplicacion/tests.py`, `api/tests.py`) están vacíos; `manage.py test` no valida nada real.

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
- Sesiones Django con `persona_id` en `request.session`; no usa el User model de Django.
