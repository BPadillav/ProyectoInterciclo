from flask import Blueprint, request, jsonify # type: ignore
from backend.services.user_service import (
    create_user, login_user, get_user_by_id, update_user, delete_user, get_all_users
)

user_bp = Blueprint('user', __name__)

# Registrar usuario
@user_bp.route('/users', methods=['POST'])
def register_user():
    """
    Registra un nuevo usuario.
    """
    try:
        data = request.get_json()
        new_user = create_user(
            email=data['email'], 
            password=data['password'], 
            username=data['username'],
            fullname =  data['fullname'],
            avatar=data.get('avatar')  # Avatar opcional
        )
        return jsonify({
            "valid": 'true',
            "id": new_user.IDuser, 
            "email": new_user.email,
            "username": new_user.username,
            "fullname": new_user.fullname,
            "avatar": new_user.avatar
        }), 201
    except ValueError as e:
        return jsonify({"valid": 'false',"error": str(e)}), 400

# Iniciar sesión
@user_bp.route('/users/login', methods=['POST'])
def login():
    """
    Permite a un usuario iniciar sesión.
    """
    try:
        data = request.get_json()
        user = login_user(data['email'], data['password'])
        return jsonify({
            "id": user.IDuser, 
            "email": user.email,
            "username": user.username,
            "fullname": user.fullname,
            "avatar": user.avatar
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

# Obtener usuario por ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Obtiene un usuario por su ID.
    """
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({
        "id": user.IDuser, 
        "email": user.email,
        "username": user.username,
        "fullname": user.fullname,
        "avatar": user.avatar
    })

# Actualizar usuario
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    """
    Actualiza la información de un usuario.
    """
    try:
        data = request.get_json()
        updated_user = update_user(
            user_id, 
            email=data.get('email'), 
            password=data.get('password'),
            username=data.get('username'),
            fullname=data.get('fullname'),
            avatar=data.get('avatar')
        )
        return jsonify({
            "id": updated_user.IDuser, 
            "email": updated_user.email,
            "username": updated_user.username,
            "fullname": updated_user.fullname,
            "avatar": updated_user.avatar
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar usuario
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_info(user_id):
    """
    Elimina un usuario por su ID.
    """
    try:
        delete_user(user_id)
        return jsonify({"message": "Usuario eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Listar todos los usuarios
@user_bp.route('/users', methods=['GET'])
def list_users():
    """
    Lista todos los usuarios registrados.
    """
    users = get_all_users()  # Asegúrate de implementar esta función en `user_service.py`
    return jsonify([
        {"id": user.IDuser, "email": user.email, "username": user.username, "fullname": user.fullname, "avatar": user.avatar}
        for user in users
    ]), 200
