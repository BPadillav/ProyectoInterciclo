from flask import Flask
from flask_cors import CORS
from backend.database.init_db import init_db  # Importa init_db
from backend.app.routes import register_routes  # Importa las rutas correctamente
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './uploads'


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Asegúrate de que el directorio exista

    # Habilita CORS para todas las rutas de la aplicación
    CORS(app, resources={r"/*": {"origins": "*"}})  # Permite solicitudes desde cualquier origen

    # Registra las rutas desde routes.py
    register_routes(app)  # Asegura que todas las rutas se registren

    # Inicializa la base de datos
    init_db(app)  # Llama a init_db pasando la aplicación

    return app

# Crear la aplicación y ejecutarla
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Hace que la aplicación esté accesible desde cualquier red
        port=5000,       # Usa el puerto 5000
        debug=True       # Activa el modo de depuración para ver errores detallados
    )
