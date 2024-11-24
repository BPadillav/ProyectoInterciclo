from backend.database.models import Likes
from database.__init__ import db as session

# Crear like
def create_like(nombrelike):
    # Crea un nuevo like
    new_like = Likes(nombrelike=nombrelike)
    session.add(new_like)
    session.commit()
    return new_like

# Obtener like por ID
def get_like_by_id(like_id):
    return session.query(Likes).filter(Likes.IDlike == like_id).first()

# Actualizar like
def update_like(like_id, nombrelike):
    like = session.query(Likes).filter(Likes.IDlike == like_id).first()
    if not like:
        raise ValueError("Like no encontrado.")
    
    like.nombrelike = nombrelike
    session.commit()
    return like

# Eliminar like
def delete_like(like_id):
    like = session.query(Likes).filter(Likes.IDlike == like_id).first()
    if not like:
        raise ValueError("Like no encontrado.")
    
    session.delete(like)
    session.commit()
    return True
