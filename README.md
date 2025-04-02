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