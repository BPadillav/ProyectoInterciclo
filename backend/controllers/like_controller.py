from flask import Blueprint, request, jsonify
from backend.services.like_service import (
    create_like, get_like_by_id, get_likes, delete_like
)

like_bp = Blueprint('like', __name__)

# Crear like
@like_bp.route('/likes', methods=['POST'])
def register_like():
    """
    Crea un nuevo like asociado a una publicación, comentario o respuesta.
    """
    try:
        data = request.get_json()
        new_like = create_like(
            userIDLike=data['user_id'],
            publicIDLike=data.get('public_id'),
            commentIDLike=data.get('comment_id'),
            answerIDLike=data.get('answer_id')
        )
        return jsonify({
            "id": new_like.IDlike,
            "user_id": new_like.userIDLike,
            "public_id": new_like.publicIDLike,
            "comment_id": new_like.commentIDLike,
            "answer_id": new_like.answerIDLike
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener like por ID
@like_bp.route('/likes/<int:like_id>', methods=['GET'])
def get_like(like_id):
    """
    Obtiene un like por su ID.
    """
    like = get_like_by_id(like_id)
    if not like:
        return jsonify({"error": "Like no encontrado"}), 404
    return jsonify({
        "id": like.IDlike,
        "user_id": like.userIDLike,
        "public_id": like.publicIDLike,
        "comment_id": like.commentIDLike,
        "answer_id": like.answerIDLike
    })

# Obtener likes por destino
@like_bp.route('/likes', methods=['GET'])
def get_likes_by_target():
    """
    Obtiene todos los likes asociados a una publicación, comentario o respuesta.
    """
    public_id = request.args.get('public_id', type=int)
    comment_id = request.args.get('comment_id', type=int)
    answer_id = request.args.get('answer_id', type=int)

    likes = get_likes(publicIDLike=public_id, commentIDLike=comment_id, answerIDLike=answer_id)

    return jsonify([
        {
            "id": like.IDlike,
            "user_id": like.userIDLike,
            "public_id": like.publicIDLike,
            "comment_id": like.commentIDLike,
            "answer_id": like.answerIDLike
        }
        for like in likes
    ]), 200

# Eliminar like
@like_bp.route('/likes/<int:like_id>', methods=['DELETE'])
def delete_like_info(like_id):
    """
    Elimina un like por su ID.
    """
    try:
        delete_like(like_id)
        return jsonify({"message": "Like eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
