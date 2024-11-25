from flask import Blueprint, request, jsonify
from backend.services.answer_service import (
    create_answer,
    get_answer_by_id,
    update_answer,
    delete_answer,
    like_answer,
    get_answers_by_comment
)
from backend.services.comment_service import get_comments_by_publicacion

answer_bp = Blueprint('answer', __name__)

# Crear respuesta
@answer_bp.route('/answers', methods=['POST'])
def register_answer():
    """
    Crea una nueva respuesta asociada a un comentario y un usuario.
    """
    try:
        data = request.get_json()
        new_answer = create_answer(
            contenido=data['contenido'],
            commentID=data['comment_id'],
            userIDAnswer=data['user_id']
        )
        return jsonify({
            "id": new_answer.IDanswer,
            "contenido": new_answer.contenido,
            "fecha": new_answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": new_answer.likes
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener todas las respuestas de un comentario
@answer_bp.route('/answers/comment/<int:comment_id>', methods=['GET'])
def get_answers_for_comment(comment_id):
    """
    Obtiene todas las respuestas asociadas a un comentario.
    """
    answers = get_answers_by_comment(comment_id, limit=None)  # Sin límite
    return jsonify([
        {
            "id": answer.IDanswer,
            "contenido": answer.contenido,
            "fecha": answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": answer.likes
        }
        for answer in answers
    ]), 200

# Obtener dos comentarios con sus respuestas
@answer_bp.route('/answers/publicacion/<int:public_id>/latest', methods=['GET'])
def get_latest_comments_with_answers(public_id):
    """
    Obtiene los dos comentarios más recientes de una publicación con sus respuestas.
    """
    comments = get_comments_by_publicacion(public_id, limit=2)  # Solo 2 comentarios
    result = []
    for comment in comments:
        answers = get_answers_by_comment(comment.IDcomments, limit=None)  # Todas las respuestas del comentario
        result.append({
            "comment": {
                "id": comment.IDcomments,
                "contenido": comment.contenido,
                "fecha": comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "likes": comment.likes
            },
            "answers": [
                {
                    "id": answer.IDanswer,
                    "contenido": answer.contenido,
                    "fecha": answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    "likes": answer.likes
                }
                for answer in answers
            ]
        })
    return jsonify(result), 200

# Actualizar respuesta
@answer_bp.route('/answers/<int:answer_id>', methods=['PUT'])
def update_answer_info(answer_id):
    """
    Actualiza el contenido de una respuesta.
    """
    try:
        data = request.get_json()
        updated_answer = update_answer(
            answer_id,
            contenido=data.get('contenido')
        )
        return jsonify({
            "id": updated_answer.IDanswer,
            "contenido": updated_answer.contenido,
            "fecha": updated_answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": updated_answer.likes
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Incrementar likes
@answer_bp.route('/answers/<int:answer_id>/like', methods=['POST'])
def like_answer_info(answer_id):
    """
    Incrementa los likes de una respuesta.
    """
    try:
        liked_answer = like_answer(answer_id)
        return jsonify({
            "id": liked_answer.IDanswer,
            "likes": liked_answer.likes
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar respuesta
@answer_bp.route('/answers/<int:answer_id>', methods=['DELETE'])
def delete_answer_info(answer_id):
    """
    Elimina una respuesta por su ID.
    """
    try:
        delete_answer(answer_id)
        return jsonify({"message": "Respuesta eliminada con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
