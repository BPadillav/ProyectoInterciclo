from backend.database.config import Config

from backend.database.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError
import time

# Crear el motor con reintentos
def get_engine_with_retries(retries=5, delay=5):
    for attempt in range(retries):
        try:
            engine = create_engine(Config.DATABASE_URL)
            with engine.connect():
                print("Conexión exitosa a la base de datos")
                return engine
        except OperationalError:
            print(f"Intento {attempt + 1} fallido, reintentando en {delay} segundos...")
            time.sleep(delay)
    raise Exception("No se pudo conectar a la base de datos después de varios intentos")

# Crear el motor
engine = get_engine_with_retries()

# Crear la sesión de la base de datos
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db(app=None):
    """Inicializa la base de datos creando tablas y configurando Flask."""
    if app:
        @app.teardown_request
        def remove_session(exception=None):
            SessionLocal.remove()

    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente.")