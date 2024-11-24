from flask import Blueprint, request, jsonify
from backend.services.user_service import (
    create_user, login_user, get_user_by_id, update_user, delete_user
)

user_bp = Blueprint('user', __name__)

# Registrar usuario
@user_bp.route('/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        new_user = create_user(data['email'], data['password'])
        return jsonify({"id": new_user.IDuser, "email": new_user.correo}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Iniciar sesión
@user_bp.route('/users/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = login_user(data['email'], data['password'])
        return jsonify({"id": user.IDuser, "email": user.correo}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

# Obtener usuario por ID
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"id": user.IDuser, "email": user.correo})

# Actualizar usuario
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    try:
        data = request.get_json()
        updated_user = update_user(
            user_id, 
            email=data.get('email'), 
            password=data.get('password')
        )
        return jsonify({"id": updated_user.IDuser, "email": updated_user.correo})
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