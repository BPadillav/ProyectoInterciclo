from flask import Blueprint, request, jsonify
from backend.services.filtro_service import create_filtro, get_filtros_by_publicacion

filtro_bp = Blueprint('filtro', __name__)

# Crear un filtro para una publicación
@filtro_bp.route('/filtros', methods=['POST'])
def add_filtro():
    try:
        data = request.get_json()
        new_filtro = create_filtro(data['nombreFiltro'], data['publicacion_id'])
        return jsonify({"id": new_filtro.IDfiltro, "nombreFiltro": new_filtro.nombreFiltro}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Obtener filtros de una publicación
@filtro_bp.route('/filtros/publicacion/<int:publicacion_id>', methods=['GET'])
def get_filtros(publicacion_id):
    filtros = get_filtros_by_publicacion(publicacion_id)
    if not filtros:
        return jsonify({"error": "No se encontraron filtros"}), 404
    return jsonify([{"id": filtro.IDfiltro, "nombreFiltro": filtro.nombreFiltro} for filtro in filtros])
