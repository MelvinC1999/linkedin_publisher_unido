from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from app.publishers.schemas import ContentType
from app.publishers.logic import Publisher
from typing import Literal, Optional, Any

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
    file: Optional[UploadFile] = File(default=None),
    image_url: Optional[str] = Form(None),
    video_url: Optional[str] = Form(None),
    document_url: Optional[str] = Form(None),
    request: Request = None,
):
    try:
        if isinstance(file, str) and file.strip() == "":
            file = None
        if isinstance(image_url, str) and image_url.strip() == "":
            image_url = None
        if isinstance(video_url, str) and video_url.strip() == "":
            video_url = None
        if isinstance(document_url, str) and document_url.strip() == "":
            document_url = None

        # ✅ Crear instancia con owner_type dinámico
        publisher = Publisher(idE=idE, owner_type=owner_type)

        # ✅ Llamar al método publicar sin repetir owner_type
        result = await publisher.publicar(
            text=text,
            content_type=content_type,
            file=file, 
            image_url=image_url,
            video_url=video_url,
            document_url=document_url
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
