# LinkedIn Publisher Unido 🚀

Proyecto en **FastAPI** que permite publicar dinámicamente **texto, imágenes, videos y documentos** en cuentas de **usuario** y **organización** de LinkedIn usando la API oficial.

---

## 🧩 Características principales

✅ Publicación de texto usando UGC (User Generated Content)  
✅ Subida y publicación de imágenes, videos y documentos  
✅ Soporte para cuentas de usuario y organización  
✅ Estructura modular y profesional en FastAPI  
✅ Manejo de tokens y URNs con `.env`  
✅ Soporte para Swagger UI ([localhost:8000/docs](http://localhost:8000/docs))  
✅ Proyecto preparado para despliegue y colaboración

---

## ⚙️ Instalación y uso

```bash
# 1. Clona el repositorio
git clone https://github.com/tu_usuario/linkedin_publisher_unido.git
cd linkedin_publisher_unido

# 2. Crea y activa el entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Crea el archivo .env con tus variables
touch .env  # o crea manualmente

# 5. Ejecuta el servidor
uvicorn main:app --reload
```

---

## 🔐 Variables de entorno (.env)

```env
LINKEDIN_ACCESS_TOKEN=tu_token_valido
DEFAULT_USER_URN=urn:li:person:xxxxxxxx
DEFAULT_ORGANIZATION_URN=urn:li:organization:xxxxxxxx
```

---

## 📬 Endpoints clave

| Método | Endpoint     | Descripción                                   |
|--------|--------------|-----------------------------------------------|
| POST   | `/publisher` | Publicar texto, imagen, video o documento     |

🧪 Todos los endpoints son interactivos desde:  
[`http://localhost:8000/docs`](http://localhost:8000/docs)

---

## 🗂️ Estructura del proyecto

```
LINKEDIN_PUBLISHER_UNIDO/
├── app/
│   ├── core/              # Configuración con Pydantic
│   ├── publishers/        # Lógica y controladores
│   │   ├── routers/       # Endpoints
│   │   ├── logic.py
│   │   ├── schemas.py
│   ├── utils/             # Herramientas auxiliares (ej. base64)
├── tests/                 # Pruebas automáticas con pytest
├── .env                   # Variables de entorno (no versionar)
├── .gitignore             # Exclusiones de Git
├── README.md              # Este archivo ✨
├── requirements.txt       # Dependencias
├── main.py                # Punto de entrada FastAPI
└── venv/                  # Entorno virtual (ignorado)
```

---

## 💻 Requisitos

- Python 3.10+
- Cuenta de LinkedIn con acceso al Developer Portal
- Permisos aprobados para publicar como usuario u organización

---

## 🙌 Autor

Desarrollado por **Melvin Cevallos**  
📧 melvin201120111@hotmail.com  
🧠 Proyecto académico y profesional