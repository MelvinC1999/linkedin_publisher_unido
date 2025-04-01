from fastapi import FastAPI
from app.core.config import settings
from app.publishers.routers import publisher

app = FastAPI()

app.include_router(publisher.router)

@app.get("/")
async def root():
    return {
        "message": "¡API de LinkedIn funcionando!",
        "user_urn": settings.DEFAULT_USER_URN,
        "organization_urn": settings.DEFAULT_ORGANIZATION_URN
    }