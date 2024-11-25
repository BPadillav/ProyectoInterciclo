from backend.database.models import Comments
from database.__init__ import db as session

# Crear comentario
def create_comment(contenido=None, image=None, userIDComment=None, publicIDComment=None):
    """
    Crea un nuevo comentario. Se debe especificar al menos contenido o una imagen.
    """
    # Validar que al menos uno de los campos esté lleno
    if not contenido and not image:
        raise ValueError("El comentario debe tener contenido o una imagen.")
    if not userIDComment or not publicIDComment:
        raise ValueError("El ID del usuario y el ID de la publicación son obligatorios.")

    # Crear un nuevo comentario
    new_comment = Comments(
        contenido=contenido,
        image=image,
        userIDComment=userIDComment,
        publicIDComment=publicIDComment
    )
    session.add(new_comment)
    session.commit()
    return new_comment

# Obtener comentario por ID
def get_comment_by_id(comment_id):
    """
    Obtiene un comentario por su ID.
    """
    return session.query(Comments).filter(Comments.IDcomments == comment_id).first()

# Obtener comentarios de una publicación
def get_comments_by_publicacion(public_id):
    """
    Obtiene todos los comentarios asociados a una publicación.
    """
    return session.query(Comments).filter(Comments.publicIDComment == public_id).all()

# Actualizar comentario
def update_comment(comment_id, contenido=None, image=None):
    """
    Actualiza el contenido o la imagen de un comentario.
    """
    comment = session.query(Comments).filter(Comments.IDcomments == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado.")

    # Validar que al menos uno de los campos esté lleno
    if not contenido and not image:
        raise ValueError("El comentario debe tener contenido o una imagen.")

    # Actualizar los campos proporcionados
    comment.contenido = contenido or comment.contenido
    comment.image = image or comment.image
    session.commit()
    return comment

# Eliminar comentario
def delete_comment(comment_id):
    """
    Elimina un comentario por su ID.
    """
    comment = session.query(Comments).filter(Comments.IDcomments == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado.")
    
    session.delete(comment)
    session.commit()
    return True
