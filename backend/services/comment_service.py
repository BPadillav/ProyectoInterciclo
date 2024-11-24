from backend.database.models import Comments, Publicaciones
from database.__init__ import db as session

# Crear un comentario y asociarlo a una publicación
def create_comment(contenido, publicacion_id):
    new_comment = Comments(contenido=contenido)
    session.add(new_comment)
    session.commit()
    
    # Asociar el comentario a la publicación
    publicacion = session.query(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).first()
    if publicacion:
        publicacion.comentPublicID = new_comment.IDcomments  # Asociar el comentario a la publicación
        session.commit()
    return new_comment

# Obtener comentarios por publicación
def get_comments_by_publicacion(publicacion_id):
    return session.query(Comments).join(Publicaciones).filter(Publicaciones.IDpublic == publicacion_id).all()
