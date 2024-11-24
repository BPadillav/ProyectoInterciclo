from backend.database.init_db import init_db

from .routes import register_routes
from .config import Config
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa la base de datos con la aplicación Flask
    init_db(app)

    # Registra las rutas
    register_routes(app)

    return app