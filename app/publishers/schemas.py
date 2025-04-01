from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class ContentType(str, Enum):
    texto = "texto"
    imagen = "imagen"
    video = "video"
    documento = "documento"