from flask import Blueprint, request, jsonify
from backend.services.comment_service import create_comment, get_comments_by_publicacion

comment_bp = Blueprint('comment', __name__)

# Crear un comentario para una publicación
@comment_bp.route('/comments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        new_comment = create_comment(data['contenido'], data['publicacion_id'])
        return jsonify({"id": new_comment.IDcomments, "contenido": new_comment.contenido}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener comentarios de una publicación
@comment_bp.route('/comments/publicacion/<int:publicacion_id>', methods=['GET'])
def get_comments(publicacion_id):
    comments = get_comments_by_publicacion(publicacion_id)
    if not comments:
        return jsonify({"error": "No se encontraron comentarios"}), 404
    return jsonify([{"id": comment.IDcomments, "contenido": comment.contenido} for comment in comments])
