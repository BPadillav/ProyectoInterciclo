from flask import Blueprint, request, jsonify
from backend.services.comment_service import (
    create_comment, 
    get_comment_by_id, 
    get_comments_by_publicacion, 
    update_comment, 
    delete_comment
)

comment_bp = Blueprint('comment', __name__)

# Crear comentario
@comment_bp.route('/comments', methods=['POST'])
def register_comment():
    """
    Crea un nuevo comentario asociado a un usuario y una publicación.
    """
    try:
        data = request.get_json()
        new_comment = create_comment(
            contenido=data.get('contenido'),
            image=data.get('image'),
            userIDComment=data['user_id'],
            publicIDComment=data['public_id']
        )
        return jsonify({
            "id": new_comment.IDcomments,
            "contenido": new_comment.contenido,
            "image": new_comment.image,
            "fecha": new_comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": new_comment.likes
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener comentario por ID
@comment_bp.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    """
    Obtiene un comentario por su ID.
    """
    comment = get_comment_by_id(comment_id)
    if not comment:
        return jsonify({"error": "Comentario no encontrado"}), 404
    return jsonify({
        "id": comment.IDcomments,
        "contenido": comment.contenido,
        "image": comment.image,
        "fecha": comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        "likes": comment.likes
    })

# Obtener comentarios de una publicación
@comment_bp.route('/comments/publicacion/<int:public_id>', methods=['GET'])
def get_comments_for_publicacion(public_id):
    """
    Obtiene todos los comentarios asociados a una publicación.
    """
    comments = get_comments_by_publicacion(public_id)
    return jsonify([
        {
            "id": comment.IDcomments,
            "contenido": comment.contenido,
            "image": comment.image,
            "fecha": comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": comment.likes
        }
        for comment in comments
    ]), 200

# Actualizar comentario
@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment_info(comment_id):
    """
    Actualiza el contenido o la imagen de un comentario.
    """
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
            "fecha": updated_comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": updated_comment.likes
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar comentario
@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment_info(comment_id):
    """
    Elimina un comentario por su ID.
    """
    try:
        delete_comment(comment_id)
        return jsonify({"message": "Comentario eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
