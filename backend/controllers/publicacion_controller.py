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
    try:
        data = request.get_json()
        new_publicacion = create_publicacion(
            ruta=data['ruta'],
            userPublicID=data['user_id'],
            comentPublicID=data.get('coment_id'),
            likePublicID=data.get('like_id'),
            filtroPublicID=data.get('filtro_id')
        )
        return jsonify({"id": new_publicacion.IDpublic, "ruta": new_publicacion.ruta}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener todas las publicaciones de un usuario
@publicacion_bp.route('/publicaciones/user/<int:user_id>', methods=['GET'])
def get_user_publicaciones(user_id):
    publicaciones = get_publicaciones_by_user(user_id)
    return jsonify([
        {"id": pub.IDpublic, "ruta": pub.ruta, "fecha": pub.fecha.strftime("%Y-%m-%d %H:%M:%S")}
        for pub in publicaciones
    ])

# Obtener una publicación por ID
@publicacion_bp.route('/publicaciones/<int:public_id>', methods=['GET'])
def get(public_id):
    publicacion = get_publicacion_by_id(public_id)
    if not publicacion:
        return jsonify({"error": "Publicación no encontrada"}), 404
    return jsonify({"id": publicacion.IDpublic, "ruta": publicacion.ruta, "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")})

# Eliminar una publicación
@publicacion_bp.route('/publicaciones/<int:public_id>', methods=['DELETE'])
def delete(public_id):
    try:
        delete_publicacion(public_id)
        return jsonify({"message": "Publicación eliminada con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Actualizar una publicación
@publicacion_bp.route('/publicaciones/<int:public_id>', methods=['PUT'])
def update(public_id):
    try:
        data = request.get_json()
        updated_publicacion = update_publicacion(
            public_id,
            ruta=data.get('ruta'),
            comentPublicID=data.get('coment_id'),
            likePublicID=data.get('like_id'),
            filtroPublicID=data.get('filtro_id')
        )
        return jsonify({"id": updated_publicacion.IDpublic, "ruta": updated_publicacion.ruta}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
