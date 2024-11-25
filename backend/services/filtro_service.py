from backend.database.models import Filtros
from database.__init__ import db as session

# Crear filtro
def create_filtro(nombreFiltro):
    """
    Crea un nuevo filtro con el nombre especificado.
    """
    if not nombreFiltro:
        raise ValueError("El nombre del filtro no puede estar vacío.")

    new_filtro = Filtros(nombreFiltro=nombreFiltro)
    session.add(new_filtro)
    session.commit()
    return new_filtro

# Obtener filtro por ID
def get_filtro_by_id(filtro_id):
    """
    Obtiene un filtro por su ID.
    """
    return session.query(Filtros).filter(Filtros.IDfiltro == filtro_id).first()

# Listar todos los filtros
def get_all_filtros():
    """
    Retorna una lista de todos los filtros disponibles.
    """
    return session.query(Filtros).all()

# Actualizar filtro
def update_filtro(filtro_id, nombreFiltro):
    """
    Actualiza el nombre de un filtro existente por su ID.
    """
    if not nombreFiltro:
        raise ValueError("El nombre del filtro no puede estar vacío.")

    filtro = session.query(Filtros).filter(Filtros.IDfiltro == filtro_id).first()
    if not filtro:
        raise ValueError("Filtro no encontrado.")
    
    filtro.nombreFiltro = nombreFiltro
    session.commit()
    return filtro

# Eliminar filtro
def delete_filtro(filtro_id):
    """
    Elimina un filtro por su ID.
    """
    filtro = session.query(Filtros).filter(Filtros.IDfiltro == filtro_id).first()
    if not filtro:
        raise ValueError("Filtro no encontrado.")
    
    session.delete(filtro)
    session.commit()
    return True
