from backend.database.models import Publicaciones, User, Comments, Likes, Filtros
from database.__init__ import db as session

# Crear una nueva publicación
def create_publicacion(user_id, ruta, coment_id=None, like_id=None, filtro_id=None):
    # Verificar si el usuario existe
    user = session.query(User).filter(User.IDuser == user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado.")

    # Crear la publicación
    nueva_publicacion = Publicaciones(
        userPublicID=user_id,
        ruta=ruta,
        comentPublicID=coment_id,
        likePublicID=like_id,
        filtroPublicID=filtro_id
    )

    session.add(nueva_publicacion)
    session.commit()

    return nueva_publicacion

# Obtener todas las publicaciones de un usuario
def get_publicaciones_by_user(user_id):
    return session.query(Publicaciones).filter(Publicaciones.userPublicID == user_id).all()

# Obtener una publicación por su ID
def get_publicacion_by_id(public_id):
    return session.query(Publicaciones).filter(Publicaciones.IDpublic == public_id).first()

# Eliminar una publicación
def delete_publicacion(public_id):
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == public_id).first()
    if not publicacion:
        raise ValueError("Publicación no encontrada.")
    
    session.delete(publicacion)
    session.commit()
    return True

# Actualizar una publicación (por ejemplo, cambiar la ruta)
def update_publicacion(public_id, ruta=None, coment_id=None, like_id=None, filtro_id=None):
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == public_id).first()
    if not publicacion:
        raise ValueError("Publicación no encontrada.")

    if ruta:
        publicacion.ruta = ruta
    if coment_id:
        publicacion.comentPublicID = coment_id
    if like_id:
        publicacion.likePublicID = like_id
    if filtro_id:
        publicacion.filtroPublicID = filtro_id

    session.commit()
    return publicacion
