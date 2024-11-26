from backend.database.models import Publicaciones
from database.__init__ import db as session

def create_publicacion(userPublicID, rutaImagen=None, contenido=None):
    """
    Crea una nueva publicación asociada a un usuario.
    """
    new_publicacion = Publicaciones(
        rutaImagen=rutaImagen,
        contenido=contenido,
        userIDPublic=userPublicID,
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

def update_publicacion(publicacion_id, rutaImagen=None, contenido=None):
    """
    Actualiza la información de una publicación.
    """
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if not publicacion:
        raise ValueError("La publicación no fue encontrada.")
    
    if rutaImagen is not None:
        publicacion.rutaImagen = rutaImagen
    if contenido is not None:
        publicacion.contenido = contenido
    

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
