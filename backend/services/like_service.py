from backend.database.models import Likes
from database.__init__ import db as session
from backend.database.models import User, Publicaciones, Comments, AnswersComments

# Crear like
def create_like(userIDLike, publicIDLike=None, commentIDLike=None, answerIDLike=None):
    """
    Crea un nuevo like asociado a una publicación, comentario o respuesta.
    """
    if not userIDLike:
        raise ValueError("El ID del usuario es obligatorio.")

    # Verificar que al menos uno de los IDs de destino esté especificado
    if not (publicIDLike or commentIDLike or answerIDLike):
        raise ValueError("El like debe estar asociado a una publicación, comentario o respuesta.")

    # Verificar que el usuario existe
    usuario = session.query(User).filter_by(IDuser=userIDLike).first()
    if not usuario:
        raise ValueError("Usuario no encontrado.")

    # Verificar que el objeto al que se le da el like existe
    if publicIDLike:
        objeto = session.query(Publicaciones).filter_by(IDpublic=publicIDLike).first()
        if not objeto:
            raise ValueError("Publicación no encontrada.")
    elif commentIDLike:
        objeto = session.query(Comments).filter_by(IDcomments=commentIDLike).first()
        if not objeto:
            raise ValueError("Comentario no encontrado.")
    elif answerIDLike:
        objeto = session.query(AnswersComments).filter_by(IDanswer=answerIDLike).first()
        if not objeto:
            raise ValueError("Respuesta no encontrada.")

    # Verificar si el usuario ya dio like al objeto
    existing_like = session.query(Likes).filter(
        Likes.userIDLike == userIDLike,
        Likes.publicIDLike == publicIDLike,
        Likes.commentIDLike == commentIDLike,
        Likes.answerIDLike == answerIDLike
    ).first()
    if existing_like:
        raise ValueError("El usuario ya ha dado like a este elemento.")

    # Crear el like
    new_like = Likes(
        userIDLike=userIDLike,
        publicIDLike=publicIDLike,
        commentIDLike=commentIDLike,
        answerIDLike=answerIDLike
    )

    session.add(new_like)
    session.commit()
    return new_like


# Obtener like por ID
def get_like_by_id(like_id):
    """
    Obtiene un like por su ID.
    """
    return session.query(Likes).filter(Likes.IDlike == like_id).first()

# Obtener likes por publicación, comentario o respuesta
def get_likes(publicIDLike=None, commentIDLike=None, answerIDLike=None):
    """
    Obtiene todos los likes asociados a una publicación, comentario o respuesta.
    """
    query = session.query(Likes)
    if publicIDLike:
        query = query.filter(Likes.publicIDLike == publicIDLike)
    if commentIDLike:
        query = query.filter(Likes.commentIDLike == commentIDLike)
    if answerIDLike:
        query = query.filter(Likes.answerIDLike == answerIDLike)
    return query.all()

# Eliminar like
def delete_like(like_id):
    """
    Elimina un like por su ID.
    """
    like = session.query(Likes).filter(Likes.IDlike == like_id).first()
    if not like:
        raise ValueError("Like no encontrado.")
    
    session.delete(like)
    session.commit()
    return True
