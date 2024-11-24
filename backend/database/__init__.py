from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from backend.database.config import Config


# Declarativa base para los modelos
Base = declarative_base()

# Configuración del motor de la base de datos
engine = create_engine(Config.DATABASE_URL)

# Crea la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Exponer db como instancia de SessionLocal
db = SessionLocal()