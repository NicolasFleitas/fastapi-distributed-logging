# models: Define la estructura de tus tablas en la base de datos

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func # Útil para el received_at automático
from database import Base # Importa la base que conecta con Postgres

class LogEntry(Base):
    """
    Define la estructura de la tabla logs en la base de datos.
    """
    __tablename__ = "logs" 

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    service = Column(String, index=True)
    severity = Column(String)
    message = Column(Text)
    received_at = Column(DateTime(timezone=True), server_default=func.now())

