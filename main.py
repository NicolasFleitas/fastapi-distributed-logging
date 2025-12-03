# Importaciones necesarias para la API, manejo de errores, seguridad y DB.
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session # Session es un objeto que representa una conexión a la base de datos
from datetime import datetime
# Importaciones locales (modelos de DB, esquemas Pydantic, conexión a DB y tokens de servicio).
import models
import schemas
import database
from config import SERVICE_TOKENS

# Inicialización crucial de la Base de Datos
# Crea la tabla 'logs' si no existe, basándose en models.py.
models.Base.metadata.create_all(bind=database.engine)

# Configuración de seguridad para usar tokens tipo Bearer (activa el botón 'Authorize' en /docs).
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, str]:
    """ 
        Verifica el token Bearer. HTTPBearer se encarga de extraerlo de la cabecera 'Authorization'. 
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
        # Respuesta estándar HTTP 401 si el token no es válido.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido. No tienes acceso a este servicio.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"✅ Autenticado: {service_name}")
    return {"token": token, "service": service_name}

app = FastAPI(title="Sistema de Logging Distribuido")

# Dependencia para gestionar la conexión a la DB.
def get_db():
    """ 
    Abre y cierra automáticamente la sesión de la DB (conexión), asegurando la limpieza. 
    """
    db = database.SessionLocal()
    try:
        yield db # 'yield' mantiene la conexión abierta hasta que el endpoint termina.
    finally:
        db.close()

# Endpoint para crear logs
@app.post("/logs", response_model=schemas.LogResponse, status_code=status.HTTP_201_CREATED)
def create_log(log: schemas.LogCreate,
               db: Session = Depends(get_db),
               auth_data: dict = Depends(verify_token)):
    """
    Recibe un log (Pydantic), verifica la autenticación y lo guarda en la base de datos.
    """
    # Convertir el esquema Pydantic a Modelo SQLAlchemy
    # **log.model_dump() convierte Pydantic a diccionario para crear el modelo SQLAlchemy.
    new_log = models.LogEntry(**log.model_dump())
    
    db.add(new_log)
    db.commit()
    # Refresca el objeto para obtener el ID y el timestamp de creación de la DB.
    db.refresh(new_log) 
    
    return new_log

# Endpoint para obtener logs
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
    Recupera una lista de logs, aplicando filtros y la política de seguridad.    
    Política de Seguridad: Solo permite ver logs del servicio asociado al token.
    """
    query = db.query(models.LogEntry)    
    
    authenticated_service = auth_data["service"]    

    # Filtro automático: Restringe la consulta a solo los logs del servicio autenticado.
    query = query.filter(models.LogEntry.service == authenticated_service)
    
    # Validación extra: Si el usuario intenta filtrar por otro servicio, se rechaza.    
    if service and service != authenticated_service:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes permiso para ver logs de '{service}'. Solo puedes ver logs de '{authenticated_service}'."
            )    
    # Filtros Opcionales (rango de tiempo/severidad)
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
    
    query = query.order_by(models.LogEntry.received_at.desc())
    
    return query.all()