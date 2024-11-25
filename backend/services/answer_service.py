from backend.database.models import AnswersComments
from database.__init__ import db as session

# Crear respuesta
def create_answer(contenido, commentID):
    if not contenido:
        raise ValueError("El contenido es obligatorio.")
    
    answer = AnswersComments(
        contenido=contenido,
        commentID=commentID
    )
    session.add(answer)
    session.commit()
    return answer

# Obtener respuesta por ID
def get_answer_by_id(answer_id):
    return session.query(AnswersComments).filter(AnswersComments.IDanswer == answer_id).first()

# Actualizar respuesta
def update_answer(answer_id, contenido=None):
    answer = session.query(AnswersComments).filter(AnswersComments.IDanswer == answer_id).first()
    if not answer:
        raise ValueError("Respuesta no encontrada.")
    
    if contenido:
        answer.contenido = contenido
    session.commit()
    return answer

# Eliminar respuesta
def delete_answer(answer_id):
    answer = session.query(AnswersComments).filter(AnswersComments.IDanswer == answer_id).first()
    if not answer:
        raise ValueError("Respuesta no encontrada.")
    
    session.delete(answer)
    session.commit()
    return True

# Incrementar likes
def like_answer(answer_id):
    answer = session.query(AnswersComments).filter(AnswersComments.IDanswer == answer_id).first()
    if not answer:
        raise ValueError("Respuesta no encontrada.")
    
    answer.likes += 1
    session.commit()
    return answer

# Obtener respuestas de un comentario (limitado a las 2 más recientes)
def get_answers_by_comment(commentID, limit=2):
    return (
        session.query(AnswersComments)
        .filter(AnswersComments.commentID == commentID)
        .order_by(AnswersComments.fecha.desc())
        .limit(limit)
        .all()
    )
