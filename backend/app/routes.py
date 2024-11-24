from flask import request, jsonify
from backend.database.init_db import get_db  # Asegúrate de importar get_db correctamente
from backend.database.models import User
def register_routes(app):
    """
    Registra todas las rutas de la aplicación Flask.

    Args:
        app (Flask): La instancia de la aplicación Flask.
    """
    @app.route('/')
    def home():
        return "Bienvenido a la API"

    @app.route('/status', methods=['GET'])
    def status():
        return {"status": "running", "message": "La API está funcionando correctamente"}, 200
    
    @app.route('/test', methods=['GET'])
    def test():
        return "Ruta de prueba exitosa"
    

    @app.route('/create_user', methods=['POST'])
    def create_user():
        data = request.get_json()

        # Usamos la sesión de base de datos a través de get_db()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Verifica si ya existe un usuario con el correo
        existing_user = db.query(User).filter(User.correo == data['correo']).first()
        if existing_user:
            return jsonify({'message': 'El usuario ya existe'}), 400

        # Si no existe, crea un nuevo usuario
        new_user = User(correo=data['correo'], contraseña=data['contraseña'])
        db.add(new_user)
        db.commit()

        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    @app.route('/list_users', methods=['GET'])
    def list_users():
        db = next(get_db())  # Obtener la sesión de base de datos
        users = db.query(User).all()  # Consulta para obtener todos los usuarios
        user_list = [{'IDuser': user.IDuser, 'correo': user.correo} for user in users]  # Crear una lista de usuarios
        return jsonify(user_list)