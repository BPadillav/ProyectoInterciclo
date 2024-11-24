

from backend.database.models import Comments
from database.__init__ import db as session

# Crear comentario
def create_comment(contenido):
    # Crea un nuevo comentario
    new_comment = Comments(contenido=contenido)
    session.add(new_comment)
    session.commit()
    return new_comment

# Obtener comentario por ID
def get_comment_by_id(comment_id):
    return session.query(Comments).filter(Comments.IDcomments == comment_id).first()

# Actualizar comentario
def update_comment(comment_id, contenido):
    comment = session.query(Comments).filter(Comments.IDcomments == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado.")
    
    comment.contenido = contenido
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
