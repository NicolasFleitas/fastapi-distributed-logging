# database: Configura la conexión a la base de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Variables para la configuración de la base de datos
DB_USER = "postgres"
DB_PASSWORD = "penguin"
DB_HOST = "localhost"
DB_NAME = "logging_db"
DB_ENCODING = "utf8"

# Formato: postgresql://usuario:password@host/nombre_base_datos?client_encoding=encoding
# Añadimos parámetros de encoding directamente en la URL
SQLALCHEMY_DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"f"?client_encoding={DB_ENCODING}")

# Creamos el motor de conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Creamos la sesión local (la usaremos para cada petición)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta clase Base la usarán tus modelos para saber que son tablas SQL
Base = declarative_base()