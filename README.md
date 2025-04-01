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

🗂️ Estructura del proyecto

```
LINKEDIN_PUBLISHER_UNIDO/
│
├── app/
│   ├── core/
│   │   └── config.py               # Configuración de entorno y tokens
│   │
│   ├── publishers/
│   │   ├── routers/
│   │   │   ├── publisher.py        # Endpoint principal para publicar
│   │   │   ├── user.py             # Obtención dinámica del user_urn
│   │   ├── logic.py                # Lógica para texto, imagen, video, documento
│   │   ├── schemas.py              # Enums y validaciones
│   │
│   ├── utils/
│   │   └── base64_tools.py         # Funciones auxiliares (si se usan)
│
├── tests/                          # Carpeta para tests
├── .env                            # Variables de entorno
├── .gitignore                      # Exclusiones de Git
├── main.py                         # Punto de entrada FastAPI
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Este archivo ✨
```


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
