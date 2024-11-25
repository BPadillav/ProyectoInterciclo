from flask import Blueprint, request, jsonify
from backend.services.comment_service import (
    create_comment, get_comment_by_id, update_comment, delete_comment
)

comment_bp = Blueprint('comment', __name__)

# Crear comentario
@comment_bp.route('/comments', methods=['POST'])
def register_comment():
    try:
        data = request.get_json()
        new_comment = create_comment(
            contenido=data.get('contenido'), 
            image=data.get('image')
        )
        return jsonify({
            "id": new_comment.IDcomments, 
            "contenido": new_comment.contenido, 
            "image": new_comment.image,
            "fecha": new_comment.fecha,
            "likes": new_comment.likes
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener comentario por ID
@comment_bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = get_comment_by_id(comment_id)
    if not comment:
        return jsonify({"error": "Comentario no encontrado"}), 404
    return jsonify({
        "id": comment.IDcomments, 
        "contenido": comment.contenido, 
        "image": comment.image,
        "fecha": comment.fecha,
        "likes": comment.likes
    })

# Actualizar comentario
@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment_info(comment_id):
    try:
        data = request.get_json()
        updated_comment = update_comment(
            comment_id, 
            contenido=data.get('contenido'), 
            image=data.get('image')
        )
        return jsonify({
            "id": updated_comment.IDcomments, 
            "contenido": updated_comment.contenido, 
            "image": updated_comment.image,
            "fecha": updated_comment.fecha,
            "likes": updated_comment.likes
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar comentario
@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment_info(comment_id):
    try:
        delete_comment(comment_id)
        return jsonify({"message": "Comentario eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
