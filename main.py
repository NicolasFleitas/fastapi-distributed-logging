# Depends es una inyección de dependencias, 
# HTTPException es para manejar errores,
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session # Session es un objeto que representa una conexión a la base de datos
from datetime import datetime
# Importamos nuestros archivos
import models
import schemas
import database
from config import SERVICE_TOKENS

# 1. Crear las tablas en la Base de Datos
# Esto revisa models.py y crea la tabla 'logs' en Postgres automáticamente.
models.Base.metadata.create_all(bind=database.engine)

# Crear el esquema de seguridad para que aparezca el botón "Authorize" en /docs
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, str]:
    """
    Esta función verifica si el token es válido.
    HTTPBearer automáticamente:
    - Verifica que el header 'Authorization' existe
    - Valida el formato "Bearer <token>"
    - Extrae el token y lo pone en credentials.credentials
    """
    token = credentials.credentials
    
    # Buscar qué servicio está haciendo la request
    service_name = None
    for service, service_token in SERVICE_TOKENS.items():
        if service_token == token:
            service_name = service
            break
    
    # Validar que el token esté en la lista VIP
    if service_name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido. No tienes acceso a este servicio.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"✅ Autenticado: {service_name}")
    return {"token": token, "service": service_name}

app = FastAPI(title="Sistema de Logging Distribuido")

# 2. Inyección de Dependencias (La magia de FastAPI)
# Esta función se encarga de abrir una conexión a la BD, entregártela para que la uses,
# y cerrarla automáticamente cuando termines, pase lo que pase (incluso si hay error).
def get_db():
    """
    Esta función se encarga de abrir una conexión a la BD, entregártela para que la uses,
    y cerrarla automáticamente cuando termines, pase lo que pase (incluso si hay error).
    """
    db = database.SessionLocal()
    try:
        yield db # yield es como un return, pero permite pausar la función hasta que se llame de nuevo
    finally:
        db.close()

# 3. Endpoint para crear logs
# response_model=schemas.LogResponse asegura que devolvemos los datos limpios (con ID y received_at)
@app.post("/logs", response_model=schemas.LogResponse, status_code=status.HTTP_201_CREATED)
def create_log(log: schemas.LogCreate,
               db: Session = Depends(get_db),
               auth_data: dict = Depends(verify_token)):
    """
    Recibe un log, lo valida y lo guarda en la base de datos.
    """
    # -Convertir el esquema Pydantic a Modelo SQLAlchemy
    # **log.model_dump() convierte el objeto en un diccionario y lo desempaqueta
    new_log = models.LogEntry(**log.model_dump()) # **log.model_dump() convierte el objeto en un diccionario y lo desempaqueta
    
    # -- Agregar a la sesión y guardar
    db.add(new_log)
    db.commit()
    db.refresh(new_log) # Recarga el objeto con los datos nuevos (como el ID generado y received_at)
    
    return new_log

# 4. Endpoint para obtener logs
@app.get("/logs", response_model=list[schemas.LogResponse])
def get_logs(
    # Filtros opcionales (Query Parameters)   
    timestamp_start: datetime | None = Query(None),
    timestamp_end: datetime | None = Query(None),
    service: str | None = Query(None),
    received_at_start: datetime | None = Query(None),
    received_at_end: datetime | None = Query(None),
    severity: str | None = Query(None),
    db: Session = Depends(get_db),
    auth_data: dict = Depends(verify_token) 
):
    """
    Obtiene una lista de logs con filtros opcionales.
    Automáticamente filtra por el servicio autenticado con el token.
    """
    query = db.query(models.LogEntry)
    
    # FILTRO AUTOMÁTICO: Solo mostrar logs del servicio autenticado
    # El servicio asociado al token actual
    authenticated_service = auth_data["service"]
    print(f"✅ Filtrando logs para: {authenticated_service}")
    query = query.filter(models.LogEntry.service == authenticated_service)
    
    # Construcción dinámica de queries
    # Solo se agrega el filtro si el usuario lo envia
    if service:
        # Si el usuario envía un filtro de servicio, validamos que coincida con su token
        if service != authenticated_service:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permiso para ver logs de '{service}'. Solo puedes ver logs de '{authenticated_service}'."
            )
        # Si coincide, el filtro ya está aplicado arriba
    
    # FILTROS OPCIONALES
    if timestamp_start:
        query = query.filter(models.LogEntry.timestamp >= timestamp_start)
    if timestamp_end:        
        query = query.filter(models.LogEntry.timestamp <= timestamp_end)
    if received_at_start:
        query = query.filter(models.LogEntry.received_at >= received_at_start)
    if received_at_end:
        query = query.filter(models.LogEntry.received_at <= received_at_end)
    if severity:
        query = query.filter(models.LogEntry.severity == severity)
    
    # Ejecutar la consulta y obtener los resultados
    return query.all()
