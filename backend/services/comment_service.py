from backend.database.models import Comments
from database.__init__ import db as session

# Crear comentario
def create_comment(contenido=None, image=None):
    if not contenido and not image:
        raise ValueError("El comentario debe tener contenido o una imagen.")

    # Crear un nuevo comentario
    new_comment = Comments(contenido=contenido, image=image)
    session.add(new_comment)
    session.commit()
    return new_comment

# Obtener comentario por ID
def get_comment_by_id(comment_id):
    return session.query(Comments).filter(Comments.IDcomments == comment_id).first()

# Actualizar comentario
def update_comment(comment_id, contenido=None, image=None):
    comment = session.query(Comments).filter(Comments.IDcomments == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado.")

    if not contenido and not image:
        raise ValueError("El comentario debe tener contenido o una imagen.")

    comment.contenido = contenido or comment.contenido
    comment.image = image or comment.image
    session.commit()
    return comment

# Eliminar comentario
def delete_comment(comment_id):
    comment = session.query(Comments).filter(Comments.IDcomments == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado.")
    
    session.delete(comment)
    session.commit()
    return True
