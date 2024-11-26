from backend.database.models import Publicaciones
from database.__init__ import db as session

# Crear publicación
def create_publicacion(ruta, userPublicID, comentPublicID=None, likePublicID=None, filtroPublicID=None):
    if not ruta:
        raise ValueError("La ruta de la imagen es obligatoria.")
    
    new_publicacion = Publicaciones(
        ruta=ruta,
        userPublicID=userPublicID,
        comentPublicID=comentPublicID,
        likePublicID=likePublicID,
        filtroPublicID=filtroPublicID
    )
    session.add(new_publicacion)
    session.commit()
    return new_publicacion

# Obtener publicaciones de un usuario
def get_publicaciones_by_user(user_id):
    return session.query(Publicaciones).filter(Publicaciones.userPublicID == user_id).all()

# Obtener publicación por ID
def get_publicacion_by_id(publicacion_id):
    return session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()

# Actualizar publicación
def update_publicacion(publicacion_id, ruta=None, comentPublicID=None, likePublicID=None, filtroPublicID=None):
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if not publicacion:
        raise ValueError("La publicación no fue encontrada.")
    
    if ruta:
        publicacion.ruta = ruta
    if comentPublicID:
        publicacion.comentPublicID = comentPublicID
    if likePublicID:
        publicacion.likePublicID = likePublicID
    if filtroPublicID:
        publicacion.filtroPublicID = filtroPublicID

    session.commit()
    return publicacion

# Eliminar publicación
def delete_publicacion(publicacion_id):
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if not publicacion:
        raise ValueError("Publicación no encontrada.")
    
    session.delete(publicacion)
    session.commit()
    return True
