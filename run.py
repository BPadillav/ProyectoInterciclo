from flask import Flask
from flask_cors import CORS
from backend.database.init_db import get_db
from backend.app.routes import register_routes  # Importa correctamente las rutas desde routes.py

def create_app():
    app = Flask(__name__)

    # Habilita CORS para todas las rutas de la aplicación
    CORS(app, resources={r"/*": {"origins": "*"}})  # Permite solicitudes desde cualquier origen

    # Registra las rutas desde routes.py
    register_routes(app)  # Se asegura de que todas las rutas se registren

    return app

# Crear la aplicación y ejecutarla
app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Hace que la aplicación esté accesible desde cualquier red
        port=5000,       # Usa el puerto 5000
        debug=True       # Activa el modo de depuración para ver errores detallados
    )
