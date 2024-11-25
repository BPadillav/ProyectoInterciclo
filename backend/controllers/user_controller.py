from flask import Blueprint, request, jsonify
from backend.services.user_service import (
    create_user, login_user, get_user_by_id, update_user, delete_user,get_all_users
)

user_bp = Blueprint('user', __name__)

# Registrar usuario
@user_bp.route('/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        new_user = create_user(
            email=data['email'], 
            password=data['password'], 
            avatar=data.get('avatar')  # Avatar opcional
        )
        return jsonify({
            "id": new_user.IDuser, 
            "email": new_user.email,
            "avatar": new_user.avatar
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Iniciar sesión
@user_bp.route('/users/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = login_user(data['email'], data['password'])
        return jsonify({
            "id": user.IDuser, 
            "email": user.email,
            "avatar": user.avatar
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

# Obtener usuario por ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({
        "id": user.IDuser, 
        "email": user.email,
        "avatar": user.avatar
    })

# Actualizar usuario
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    try:
        data = request.get_json()
        updated_user = update_user(
            user_id, 
            email=data.get('email'), 
            password=data.get('password'),
            avatar=data.get('avatar')
        )
        return jsonify({
            "id": updated_user.IDuser, 
            "email": updated_user.email,
            "avatar": updated_user.avatar
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar usuario
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_info(user_id):
    try:
        delete_user(user_id)
        return jsonify({"message": "Usuario eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@user_bp.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()  # Asegúrate de implementar esta función en `user_service.py`
    return jsonify([
        {"id": user.IDuser, "email": user.email, "avatar": user.avatar}
        for user in users
    ]), 200

