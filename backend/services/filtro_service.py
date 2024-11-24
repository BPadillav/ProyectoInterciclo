from backend.database.models import Filtros, Publicaciones
from database.__init__ import db as session

# Crear un filtro y asociarlo a una publicación
def create_filtro(nombre_filtro, publicacion_id):
    new_filtro = Filtros(nombreFiltro=nombre_filtro)
    session.add(new_filtro)
    session.commit()
    
    # Asociar el filtro a la publicación
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if publicacion:
        publicacion.filtroPublicID = new_filtro.IDfiltro  # Asociar el filtro a la publicación
        session.commit()
    return new_filtro

# Obtener filtros por publicación
def get_filtros_by_publicacion(publicacion_id):
    return session.query(Filtros).join(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).all()
