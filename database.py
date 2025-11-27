# database: Configura la conexión a la base de datos

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
    
# Formato: postgresql://usuario:password@localhost/nombre_base_datos
# Añadimos parámetros de encoding directamente en la URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:penguin@localhost/logging_db?client_encoding=utf8"

# Creamos el motor de conexión
# pool_pre_ping verifica la conexión antes de usarla
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# Creamos la sesión local (la usaremos para cada petición)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta clase Base la usarán tus modelos para saber que son tablas SQL
Base = declarative_base()