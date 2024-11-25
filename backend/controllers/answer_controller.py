from flask import Blueprint, request, jsonify
from backend.services.answer_service import (
    create_answer,
    get_answer_by_id,
    update_answer,
    delete_answer,
    like_answer,
    get_answers_by_comment,
)

answer_bp = Blueprint('answer', __name__)

# Crear respuesta
@answer_bp.route('/answers', methods=['POST'])
def create():
    """
    Crea una nueva respuesta asociada a un comentario.
    """
    try:
        data = request.get_json()
        answer = create_answer(
            contenido=data['contenido'],
            commentID=data['comment_id'],
            userIDAnswer=data['user_id']
        )
        return jsonify({
            "id": answer.IDanswer,
            "contenido": answer.contenido,
            "fecha": answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": answer.likes
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener respuesta por ID
@answer_bp.route('/answers/<int:answer_id>', methods=['GET'])
def get(answer_id):
    """
    Obtiene una respuesta específica por su ID.
    """
    answer = get_answer_by_id(answer_id)
    if not answer:
        return jsonify({"error": "Respuesta no encontrada"}), 404
    return jsonify({
        "id": answer.IDanswer,
        "contenido": answer.contenido,
        "fecha": answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
        "likes": answer.likes
    })

# Actualizar respuesta
@answer_bp.route('/answers/<int:answer_id>', methods=['PUT'])
def update(answer_id):
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

# Eliminar respuesta
@answer_bp.route('/answers/<int:answer_id>', methods=['DELETE'])
def delete(answer_id):
    """
    Elimina una respuesta por su ID.
    """
    try:
        delete_answer(answer_id)
        return jsonify({"message": "Respuesta eliminada con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Incrementar likes
@answer_bp.route('/answers/<int:answer_id>/like', methods=['POST'])
def like(answer_id):
    """
    Incrementa los likes de una respuesta.
    """
    try:
        updated_answer = like_answer(answer_id)
        return jsonify({
            "id": updated_answer.IDanswer,
            "likes": updated_answer.likes
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener respuestas de un comentario
@answer_bp.route('/answers/comment/<int:comment_id>', methods=['GET'])
def get_by_comment(comment_id):
    """
    Obtiene todas las respuestas asociadas a un comentario.
    """
    answers = get_answers_by_comment(comment_id, limit=None)  # Todas las respuestas
    return jsonify([
        {
            "id": answer.IDanswer,
            "contenido": answer.contenido,
            "fecha": answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": answer.likes
        }
        for answer in answers
    ]), 200



