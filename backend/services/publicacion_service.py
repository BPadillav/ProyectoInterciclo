from backend.database.models import Publicaciones
from database.__init__ import db as session

# Crear publicación
def create_publicacion(rutaImagen, userPublicID, contenido=None, filtroIDPublic=None):
    """
    Crea una nueva publicación asociada a un usuario.
    """
    if not rutaImagen:
        raise ValueError("La ruta de la imagen es obligatoria.")
    
    new_publicacion = Publicaciones(
        rutaImagen=rutaImagen,
        contenido=contenido,
        userIDPublic=userPublicID,
        filtroIDPublic=filtroIDPublic
    )
    session.add(new_publicacion)
    session.commit()
    return new_publicacion

# Obtener publicaciones de un usuario
def get_publicaciones_by_user(user_id):
    """
    Obtiene todas las publicaciones asociadas a un usuario.
    """
    return session.query(Publicaciones).filter(Publicaciones.userIDPublic == user_id).all()

# Obtener publicación por ID
def get_publicacion_by_id(publicacion_id):
    """
    Obtiene una publicación específica por su ID.
    """
    return session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()

# Actualizar publicación
def update_publicacion(publicacion_id, rutaImagen=None, contenido=None, filtroIDPublic=None):
    """
    Actualiza la información de una publicación.
    """
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if not publicacion:
        raise ValueError("La publicación no fue encontrada.")
    
    if rutaImagen:
        publicacion.rutaImagen = rutaImagen
    if contenido:
        publicacion.contenido = contenido
    if filtroIDPublic:
        publicacion.filtroIDPublic = filtroIDPublic

    session.commit()
    return publicacion

# Eliminar publicación
def delete_publicacion(publicacion_id):
    """
    Elimina una publicación por su ID.
    """
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if not publicacion:
        raise ValueError("Publicación no encontrada.")
    
    session.delete(publicacion)
    session.commit()
    return True
