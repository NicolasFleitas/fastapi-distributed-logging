# schemas: Definen como se ven los datos en la API (entrada y salida)

from pydantic import BaseModel
from datetime import datetime


# Sirve para no repetir el código
class LogBase(BaseModel):
    """
    Campos base compartidos por todos los modelos de log.
    """
    service: str
    severity: str
    message: str

class LogCreate(LogBase):
    """
    Datos requeridos para crear un nuevo log (incluye timestamp del evento).
    """
    timestamp: datetime

class LogResponse(LogBase):
    """
    Respuesta del servidor al crear/obtener logs (incluye ID y received_at).
    """
    id: int
    received_at: datetime

    class Config:
        from_attributes = True
    # Truco: Para que Pydantic lea datos de un modelo ORM (SQLAlchemy),
    # necesitas agregar una configuración interna: model_config = ConfigDict(from_attributes=True

