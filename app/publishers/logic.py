from fastapi import UploadFile
from app.core.config import settings
import httpx
import uuid
from pathlib import Path
from app.publishers.routers.user import get_user_info  # Asegúrate de tenerlo implementado

# Simulación temporal de una "base de datos" de tokens
FAKE_DB = {
    "user123": settings.LINKEDIN_ACCESS_TOKEN
}

class Publisher:
    def __init__(self, idE: str, owner_type: str):
        self.idE = idE
        self.owner_type = owner_type
        self.access_token = self._get_token_from_db()
        self.urn = self._get_dynamic_urn()  # Dinámico para usuario u organización

        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "LinkedIn-Version": "202503",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }

    def _get_token_from_db(self) -> str:
        if self.idE not in FAKE_DB:
            raise ValueError("Token no encontrado para el idE proporcionado.")
        return FAKE_DB[self.idE]

    def _get_dynamic_urn(self) -> str:
        if self.owner_type == "organization":
            return settings.DEFAULT_ORGANIZATION_URN
        else:
            user_info = get_user_info()
            return user_info.get("user_urn", settings.DEFAULT_USER_URN)

    async def publicar(self, text: str, content_type: str, file: UploadFile = None, image_url: str = None, video_url: str = None, document_url: str = None):
        if content_type == "texto":
            return await self._publicar_texto(text)
        elif content_type == "imagen":
            return await self._publicar_imagen(text, file, image_url)
        elif content_type == "video":
            return await self._publicar_video(text, file, video_url)
        elif content_type == "documento":
            return await self._publicar_documento(text, file, document_url)
        else:
            raise NotImplementedError(f"Tipo de contenido '{content_type}' no implementado aún.")

    async def _publicar_texto(self, text: str):
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Linkedin-Version": "202503",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        payload = {
            "author": self.urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            try:
                data = response.json()
            except Exception:
                data = response.text

        if response.status_code == 201:
            return {"status": "success", "message": "✅ Publicado como usuario con UGC", "data": data}
        else:
            return {"status": "error", "message": f"❌ Error al publicar UGC ({response.status_code})", "data": data}


    async def _descargar_desde_url(self, url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.content, response.headers.get("content-type")
            else:
                raise Exception(f"Error al descargar archivo desde la URL: {response.status_code}")

            
    async def _publicar_imagen(self, text: str, file: UploadFile, image_url: str = None):
        if file and hasattr(file, "read"):
            file_bytes = await file.read()
            mime_type = file.content_type
        elif image_url:
            file_bytes, mime_type = await self._descargar_desde_url(image_url)
        else:
            return {
                "status": "error",
                "message": "Debes proporcionar un archivo válido o una URL de imagen válida."
            }

        if not mime_type.startswith("image/"):
            return {"status": "error", "message": f"Tipo de archivo no válido: {mime_type}"}

        # 1️⃣ Inicializar subida
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        register_payload = {
            "registerUploadRequest": {
                "owner": self.urn,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ],
                "supportedUploadMechanism": ["SYNCHRONOUS_UPLOAD"]
            }
        }

        async with httpx.AsyncClient() as client:
            register_response = await client.post(register_url, json=register_payload, headers=self.headers)

        if register_response.status_code != 200:
            return {
                "status": "error",
                "message": "Error al inicializar subida de imagen",
                "data": register_response.text
            }

        register_data = register_response.json()["value"]
        upload_url = register_data["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_urn = register_data["asset"]

        # 2️⃣ Subir archivo
        upload_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }

        async with httpx.AsyncClient() as client:
            upload_response = await client.put(upload_url, content=file_bytes, headers=upload_headers)

        if upload_response.status_code != 201:
            return {
                "status": "error",
                "message": "Error al subir la imagen",
                "data": upload_response.text
            }

        # 3️⃣ Publicar post con imagen
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        post_payload = {
            "author": self.urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn,
                            "title": {
                                "text": "📸 Imagen desde FastAPI"
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        async with httpx.AsyncClient() as client:
            post_response = await client.post(post_url, json=post_payload, headers=self.headers)

        try:
            post_data = post_response.json()
        except Exception:
            post_data = post_response.text

        if post_response.status_code == 201:
            return {
                "status": "success",
                "message": "✅ Imagen publicada exitosamente",
                "data": post_data
            }
        else:
            return {
                "status": "error",
                "message": f"Error al publicar imagen ({post_response.status_code})",
                "data": post_data
            }


    async def _publicar_video(self, text: str, file: UploadFile, video_url: str = None):
        if file and hasattr(file, "read"):
            file_bytes = await file.read()
            mime_type = file.content_type
        elif video_url:
            file_bytes, mime_type = await self._descargar_desde_url(video_url)
        else:
            return {"status": "error", "message": "Debes proporcionar un archivo o una URL de video válida."}

        if not mime_type.startswith("video/"):
            return {"status": "error", "message": f"Tipo de archivo no válido: {mime_type}"}

        # 1️⃣ Registrar subida del video
        register_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        register_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Linkedin-Version": "202503",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        register_payload = {
            "registerUploadRequest": {
                "owner": self.urn,
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-video"],
                "serviceRelationships": [
                    {
                        "identifier": "urn:li:userGeneratedContent",
                        "relationshipType": "OWNER"
                    }
                ],
                "supportedUploadMechanism": ["SINGLE_REQUEST_UPLOAD"]
            }
        }

        async with httpx.AsyncClient() as client:
            register_response = await client.post(register_url, json=register_payload, headers=register_headers)

        if register_response.status_code != 200:
            return {
                "status": "error",
                "message": "Error al registrar subida de video",
                "data": register_response.text
            }

        register_data = register_response.json()
        upload_url = register_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_urn = register_data["value"]["asset"]

        # 2️⃣ Subir video binario
        upload_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }

        async with httpx.AsyncClient() as client:
            upload_response = await client.put(upload_url, content=file_bytes, headers=upload_headers)

        if upload_response.status_code not in [200, 201]:
            return {
                "status": "error",
                "message": "Error al subir el video",
                "data": upload_response.text
            }

        # 3️⃣ Publicar post con el video
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        post_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

        post_payload = {
            "author": self.urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "VIDEO",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_urn,
                            "title": {
                                "text": "Video desde FastAPI"
                            },
                            "description": {
                                "text": "Subido vía UGC con FastAPI"
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        async with httpx.AsyncClient() as client:
            post_response = await client.post(post_url, json=post_payload, headers=post_headers)

        try:
            post_data = post_response.json()
        except Exception:
            post_data = post_response.text

        if post_response.status_code == 201:
            return {
                "status": "success",
                "message": "✅ Video publicado exitosamente",
                "data": post_data
            }
        else:
            return {
                "status": "error",
                "message": f"Error al publicar video ({post_response.status_code})",
                "data": post_data
            }
        
    # Paso 1: Validaciones
    def is_valid_document_type(self, mime_type: str) -> bool:
        return mime_type in [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]

    async def _publicar_documento(self, text: str, file: UploadFile, document_url: str = None):
        if file and hasattr(file, "read"):
            file_bytes = await file.read()
            mime_type = file.content_type
        elif document_url:
            file_bytes, mime_type = await self._descargar_desde_url(document_url)
        else:
            return {"status": "error", "message": "Debes proporcionar un archivo de documento o una URL válida."}
        
        if self.owner_type != "organization":
            return {"status": "error", "message": "Solo las organizaciones pueden publicar documentos."}

        if not self.is_valid_document_type(mime_type):
            return {"status": "error", "message": f"Tipo de documento no permitido: {mime_type}"}

        # 1️⃣ Inicializar subida
        register_url = "https://api.linkedin.com/rest/documents?action=initializeUpload"
        register_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Linkedin-Version": "202503",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        register_payload = {
            "initializeUploadRequest": {
                "owner": self.urn
            }
        }

        async with httpx.AsyncClient() as client:
            register_response = await client.post(register_url, json=register_payload, headers=register_headers)

        if register_response.status_code != 200:
            return {
                "status": "error",
                "message": "Error al registrar el documento",
                "data": register_response.text
            }

        register_data = register_response.json()["value"]
        upload_url = register_data["uploadUrl"]
        document_urn = register_data["document"]

        # 2️⃣ Subir archivo binario
        upload_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }

        async with httpx.AsyncClient() as client:
            upload_response = await client.put(upload_url, content=file_bytes, headers=upload_headers)

        if upload_response.status_code not in [200, 201]:
            return {
                "status": "error",
                "message": "Error al subir el documento",
                "data": upload_response.text
            }

        # 3️⃣ Publicar post
        post_url = "https://api.linkedin.com/rest/posts"
        post_payload = {
            "author": self.urn,
            "commentary": text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": []
            },
            "content": {
                "media": {
                    "title": "Documento Subido desde FastAPI",
                    "id": document_urn
                }
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False
        }

        async with httpx.AsyncClient() as client:
            post_response = await client.post(post_url, json=post_payload, headers=register_headers)

        try:
            post_data = post_response.json()
        except Exception:
            post_data = post_response.text

        if post_response.status_code == 201:
            return {
                "status": "success",
                "message": "✅ Documento publicado exitosamente como organización",
                "data": post_data
            }
        else:
            return {
                "status": "error",
                "message": f"Error al publicar documento ({post_response.status_code})",
                "data": post_data
            }