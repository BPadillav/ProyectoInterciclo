from backend.database.models import Filtros
from database.__init__ import db as session

# Crear filtro
def create_filtro(nombreFiltro):
    # Crea un nuevo filtro
    new_filtro = Filtros(nombreFiltro=nombreFiltro)
    session.add(new_filtro)
    session.commit()
    return new_filtro

# Obtener filtro por ID
def get_filtro_by_id(filtro_id):
    return session.query(Filtros).filter(Filtros.IDfiltro == filtro_id).first()

# Actualizar filtro
def update_filtro(filtro_id, nombreFiltro):
    filtro = session.query(Filtros).filter(Filtros.IDfiltro == filtro_id).first()
    if not filtro:
        raise ValueError("Filtro no encontrado.")
    
    filtro.nombreFiltro = nombreFiltro
    session.commit()
    return filtro

# Eliminar filtro
def delete_filtro(filtro_id):
    filtro = session.query(Filtros).filter(Filtros.IDfiltro == filtro_id).first()
    if not filtro:
        raise ValueError("Filtro no encontrado.")
    
    session.delete(filtro)
    session.commit()
    return True
