from flask import Blueprint, request, jsonify
from backend.services.publicacion_service import (
    create_publicacion, 
    get_publicaciones_by_user, 
    get_publicacion_by_id, 
    delete_publicacion, 
    update_publicacion
)

publicacion_bp = Blueprint('publicacion', __name__)

# Crear una publicación
@publicacion_bp.route('/publicaciones', methods=['POST'])
def create():
    """
    Crea una nueva publicación.
    """
    try:
        data = request.get_json()
        new_publicacion = create_publicacion(
            userPublicID=data['user_id'],
            contenido=data.get('contenido'),
        )
        return jsonify({
            "id": new_publicacion.IDpublic, 
            "contenido": new_publicacion.contenido,
            "fecha": new_publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener todas las publicaciones de un usuario
@publicacion_bp.route('/publicaciones/user/<int:user_id>', methods=['GET'])
def get_user_publicaciones(user_id):
    """
    Obtiene todas las publicaciones de un usuario específico.
    """
    publicaciones = get_publicaciones_by_user(user_id)
    return jsonify([
        {
            "id": pub.IDpublic,
            "contenido": pub.contenido,
            "fecha": pub.fecha.strftime("%Y-%m-%d %H:%M:%S")
        }
        for pub in publicaciones
    ]), 200

# Obtener una publicación por ID
@publicacion_bp.route('/publicaciones/<int:public_id>', methods=['GET'])
def get(public_id):
    """
    Obtiene una publicación por su ID.
    """
    publicacion = get_publicacion_by_id(public_id)
    if not publicacion:
        return jsonify({"error": "Publicación no encontrada"}), 404
    return jsonify({
        "id": publicacion.IDpublic,
        "contenido": publicacion.contenido,
        "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

# Eliminar una publicación
@publicacion_bp.route('/publicaciones/<int:public_id>', methods=['DELETE'])
def delete(public_id):
    """
    Elimina una publicación por su ID.
    """
    try:
        delete_publicacion(public_id)
        return jsonify({"message": "Publicación eliminada con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Actualizar una publicación
@publicacion_bp.route('/publicaciones/<int:public_id>', methods=['PUT'])
def update(public_id):
    """
    Actualiza una publicación existente.
    """
    try:
        data = request.get_json()
        updated_publicacion = update_publicacion(
            public_id,
            contenido=data.get('contenido'),
        )
        return jsonify({
            "id": updated_publicacion.IDpublic,
            "contenido": updated_publicacion.contenido,
            "fecha": updated_publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
