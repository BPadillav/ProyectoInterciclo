from flask import Blueprint, request, jsonify
from backend.services.filtro_service import (
    create_filtro, get_filtro_by_id, update_filtro, delete_filtro
)

filtro_bp = Blueprint('filtro', __name__)

# Crear filtro
@filtro_bp.route('/filtros', methods=['POST'])
def register_filtro():
    try:
        data = request.get_json()
        new_filtro = create_filtro(data['nombreFiltro'])
        return jsonify({"id": new_filtro.IDfiltro, "nombreFiltro": new_filtro.nombreFiltro}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener filtro por ID
@filtro_bp.route('/filtros/<int:filtro_id>', methods=['GET'])
def get_filtro(filtro_id):
    filtro = get_filtro_by_id(filtro_id)
    if not filtro:
        return jsonify({"error": "Filtro no encontrado"}), 404
    return jsonify({"id": filtro.IDfiltro, "nombreFiltro": filtro.nombreFiltro})

# Actualizar filtro
@filtro_bp.route('/filtros/<int:filtro_id>', methods=['PUT'])
def update_filtro_info(filtro_id):
    try:
        data = request.get_json()
        updated_filtro = update_filtro(filtro_id, nombreFiltro=data.get('nombreFiltro'))
        return jsonify({"id": updated_filtro.IDfiltro, "nombreFiltro": updated_filtro.nombreFiltro})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Eliminar filtro
@filtro_bp.route('/filtros/<int:filtro_id>', methods=['DELETE'])
def delete_filtro_info(filtro_id):
    try:
        delete_filtro(filtro_id)
        return jsonify({"message": "Filtro eliminado con éxito"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
