from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from app.publishers.schemas import ContentType
from app.publishers.logic import Publisher
from typing import Literal

router = APIRouter(
    prefix="",
    tags=["LinkedIn Publisher"]
)

@router.post("/publisher", summary="Publica contenido en LinkedIn")
async def publish_content(
    idE: str = Form(...),
    text: str = Form(...),
    content_type: ContentType = Form(...),
    owner_type: Literal["user", "organization"] = Form(...),
    file: UploadFile = File(None),
    request: Request = None,
):
    try:
        # ✅ Crear instancia con owner_type dinámico
        publisher = Publisher(idE=idE, owner_type=owner_type)

        # ✅ Llamar al método publicar sin repetir owner_type
        result = await publisher.publicar(
            text=text,
            content_type=content_type,
            file=file
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
