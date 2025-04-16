# LinkedIn Publisher Unido 🚀

Este proyecto desarrollado en **FastAPI** permite realizar publicaciones dinámicas en LinkedIn usando su API oficial, ya sea como usuario o como organización.

## 🔧 Funcionalidades implementadas

- ✅ Publicaciones de texto (UGC)
- ✅ Imágenes (UGC)
- ✅ Videos (UGC)
- ✅ Documentos (solo como organización)
- 🧠 Publicación dinámica: elige entre usuario u organización
- 🔒 Uso de tokens y URNs desde archivo `.env`

## 🏗️ Estructura del Proyecto

```
LINKEDIN_PUBLISHER_UNIDO/
│
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configuración principal (settings de Pydantic)
│   │
│   ├── publishers/
│       ├── __init__.py
│       ├── logic.py           # Clase Publisher con métodos de publicación
│       ├── schemas.py         # Esquemas Pydantic (request/response)
│       │
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── publisher.py   # POST /publisher (endpoint principal)
│       │   └── user.py        # GET /userinfo (obtener user_urn)
│       │
│       └── utils/
│           ├── __init__.py
│           └── base64_tools.py # decode_base64_file, validate_mime_type
│ 
│
├── tests/
│   ├── __init__.py
│   ├── test_publisher.py      # Tests para endpoints
│   └── conftest.py            # Fixtures de pytest
│
├── .env                       # Variables sensibles (NO versionar)
├── .gitignore                 # Ignorar venv, .env, __pycache__
├── README.md                  # Instrucciones de instalación y uso
├── requirements.txt           # Dependencias (FastAPI, SQLAlchemy, etc.)
├── main.py                    # App FastAPI + configuración global
└── venv/                      # Entorno virtual (ignorado por git)
=======
📢 LinkedIn Publisher Unido 🚀

Proyecto en FastAPI que permite publicar dinámicamente **texto, imágenes, videos y documentos** en cuentas de **usuario** y **organización** de LinkedIn usando la API oficial.

---

🧩 Características principales

✅ Publicación de texto usando UGC (User Generated Content)  
✅ Subida y publicación de imágenes, videos y documentos  
✅ Soporte para cuentas de usuario y organización  
✅ Estructura modular y profesional en FastAPI  
✅ Manejo de tokens y URNs con `.env`  
✅ Soporte para Swagger UI (http://localhost:8000/docs)  
✅ Proyecto preparado para despliegue y colaboración

---

⚙️ Instalación y uso

```bash
# 1. Clona el repositorio
git clone https://github.com/tu_usuario/linkedin_publisher_unido.git
cd linkedin_publisher_unido

# 2. Crea y activa el entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Configura tus variables en .env
touch .env  # O crea el archivo manualmente

# 5. Ejecuta el servidor
uvicorn main:app --reload
```

---

🔐 Variables de entorno (.env)

```env
LINKEDIN_ACCESS_TOKEN=tu_token_valido
DEFAULT_USER_URN=urn:li:person:xxxxxxxx
DEFAULT_ORGANIZATION_URN=urn:li:organization:xxxxxxxx
```


📬 Endpoints clave

| Método | Endpoint        | Descripción                       |
|--------|------------------|-----------------------------------|
| POST   | `/publisher`     | Publicar texto, imagen, video o documento |

Todos los métodos se pueden probar fácilmente desde Swagger:  
📍 [`http://localhost:8000/docs`](http://localhost:8000/docs)


💻 Requisitos

- Python 3.10+
- Cuenta de LinkedIn con acceso a Developer Portal
- Permisos para publicar en LinkedIn (usuario y/o organización)

🙌 Autor

Desarrollado por **Melvin Cevallos**  
🧠 Proyecto académico y profesional
