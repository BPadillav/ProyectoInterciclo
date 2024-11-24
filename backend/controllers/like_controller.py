from flask import Blueprint, request, jsonify
from backend.services.likes_service import create_like, get_likes_by_publicacion

like_bp = Blueprint('like', __name__)

# Crear un like para una publicación
@like_bp.route('/likes', methods=['POST'])
def add_like():
    try:
        data = request.get_json()
        new_like = create_like(data['nombrelike'], data['publicacion_id'])
        return jsonify({"id": new_like.IDlike, "nombrelike": new_like.nombrelike}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener likes de una publicación
@like_bp.route('/likes/publicacion/<int:publicacion_id>', methods=['GET'])
def get_likes(publicacion_id):
    likes = get_likes_by_publicacion(publicacion_id)
    if not likes:
        return jsonify({"error": "No se encontraron likes"}), 404
    return jsonify([{"id": like.IDlike, "nombrelike": like.nombrelike} for like in likes])
