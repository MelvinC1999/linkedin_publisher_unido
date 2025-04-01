import base64
import re
from typing import Tuple

def decode_base64_file(data_base64: str) -> Tuple[str, bytes]:
    """
    Decodifica un archivo en base64 con encabezado MIME.
    Retorna una tupla (mime_type, file_bytes).
    """
    # Ejemplo esperado: data:image/jpeg;base64,/9j/4AAQSk...
    pattern = r"^data:(.+);base64,(.+)"
    match = re.match(pattern, data_base64)

    if not match:
        raise ValueError("Formato base64 inválido. Asegúrate de incluir el encabezado MIME.")

    mime_type = match.group(1)
    base64_data = match.group(2)

    try:
        file_bytes = base64.b64decode(base64_data)
    except Exception as e:
        raise ValueError("Error al decodificar base64: " + str(e))

    return mime_type, file_bytes