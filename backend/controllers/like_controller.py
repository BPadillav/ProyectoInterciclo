from flask import Blueprint, request, jsonify
from backend.services.like_service import (
    create_like, get_like_by_id, update_like, delete_like
)

like_bp = Blueprint('like', __name__)

# Crear like
@like_bp.route('/likes', methods=['POST'])
def register_like():
    try:
        data = request.get_json()
        new_like = create_like(data['nombrelike'])
        return jsonify({"id": new_like.IDlike, "nombrelike": new_like.nombrelike}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener like por ID
@like_bp.route('/likes/<int:like_id>', methods=['GET'])
def get_like(like_id):
    like = get_like_by_id(like_id)
    if not like:
        return jsonify({"error": "Like no encontrado"}), 404
    return jsonify({"id": like.IDlike, "nombrelike": like.nombrelike})

# Actualizar like
@like_bp.route('/likes/<int:like_id>', methods=['PUT'])
def update_like_info(like_id):
    try:
        data = request.get_json()
        updated_like = update_like(like_id, nombrelike=data.get('nombrelike'))
        return jsonify({"id": updated_like.IDlike, "nombrelike": updated_like.nombrelike})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar like
@like_bp.route('/likes/<int:like_id>', methods=['DELETE'])
def delete_like_info(like_id):
    try:
        delete_like(like_id)
        return jsonify({"message": "Like eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
