from flask import Flask
from flask_cors import CORS  # Importa la extensión Flask-CORS
from backend.app import create_app

def create_app():
    app = Flask(__name__)

    # Aquí agregamos CORS a la aplicación
    CORS(app)  # Esto habilita CORS para todas las rutas de la aplicación

    # Otras configuraciones y rutas
    return app

app = create_app()

if __name__ == '__main__':
    # Ejecuta la aplicación con soporte para HTTP
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
