from backend.database.models import Likes, Publicaciones
from database.__init__ import db as session

# Crear un like y asociarlo a una publicación
def create_like(nombrelike, publicacion_id):
    new_like = Likes(nombrelike=nombrelike)
    session.add(new_like)
    session.commit()
    
    # Asociar el like a la publicación
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if publicacion:
        publicacion.likePublicID = new_like.IDlike  # Asociar el like a la publicación
        session.commit()
    return new_like

# Obtener likes por publicación
def get_likes_by_publicacion(publicacion_id):
    return session.query(Likes).join(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).all()
