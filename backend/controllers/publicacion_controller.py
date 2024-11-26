from flask import Blueprint, request, jsonify
from backend.services.publicacion_service import (
    create_publicacion, 
    get_publicaciones_by_user, 
    get_publicacion_by_id, 
    delete_publicacion, 
    update_publicacion
)

publicacion_bp = Blueprint('publicacion', __name__)

@publicacion_bp.route('/publicaciones', methods=['POST'])
def create():
    """
    Crea una nueva publicación.
    """
    try:
        ruta_imagen = request.files.get('rutaImagen')
        contenido = request.form.get('contenido')
        user_id = request.form.get('user_id')
        filtro_id = request.form.get('filtro_id')

        if not ruta_imagen and not contenido:
            raise ValueError("Debe proporcionar al menos una imagen o contenido para la publicación.")
        if not user_id:
            raise ValueError("El ID de usuario es obligatorio.")

        # Manejar la imagen (si se proporciona)
        imagen_path = None
        if ruta_imagen:
            # Validar el nombre del archivo directamente
            filename = ruta_imagen.filename

            # Reemplazar caracteres inseguros manualmente
            filename = filename.replace(" ", "_").replace("..", "_")

            # Guardar el archivo en la carpeta 'uploads'
            imagen_path = f"uploads/{filename}"
            ruta_imagen.save(imagen_path)

        # Crear la publicación
        new_publicacion = create_publicacion(
            rutaImagen=imagen_path,
            userPublicID=user_id,
            contenido=contenido,
            filtroIDPublic=filtro_id
        )

        return jsonify({
            "id": new_publicacion.IDpublic,
            "rutaImagen": new_publicacion.rutaImagen,
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
            "rutaImagen": pub.rutaImagen,
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
        "rutaImagen": publicacion.rutaImagen,
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
            rutaImagen=data.get('rutaImagen'),
            contenido=data.get('contenido'),
            filtroIDPublic=data.get('filtro_id')
        )
        return jsonify({
            "id": updated_publicacion.IDpublic,
            "rutaImagen": updated_publicacion.rutaImagen,
            "contenido": updated_publicacion.contenido,
            "fecha": updated_publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
