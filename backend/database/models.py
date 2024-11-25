from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Tabla User
class User(Base):
    __tablename__ = "users"

    IDuser = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)  # Nuevo campo para la imagen de avatar

    publicaciones = relationship("Publicaciones", back_populates="usuario")
    comentarios = relationship("Comments", back_populates="usuario")
    likes = relationship("Likes", back_populates="usuario")
    respuestas = relationship("AnswersComments", back_populates="usuario")


# Tabla Filtros
class Filtros(Base):
    __tablename__ = "filtros"

    IDfiltro = Column(Integer, primary_key=True, autoincrement=True)
    nombreFiltro = Column(String(255), nullable=False)

    publicaciones = relationship("Publicaciones", back_populates="filtro")


# Tabla Publicaciones
class Publicaciones(Base):
    __tablename__ = "publicaciones"

    IDpublic = Column(Integer, primary_key=True, autoincrement=True)
    rutaImagen = Column(String(255), nullable=True)  # Ruta de la imagen subida
    contenido = Column(Text, nullable=True)  # Contenido de texto asociado a la publicación
    fecha = Column(DateTime, default=datetime.utcnow)  # Fecha de creación de la publicación

    # Foreign Keys
    userIDPublic = Column(Integer, ForeignKey("users.IDuser"), nullable=False)  # Usuario que hizo la publicación
    filtroIDPublic = Column(Integer, ForeignKey("filtros.IDfiltro"), nullable=True)  # Filtro asociado (si aplica)

    # Relationships
    usuario = relationship("User", back_populates="publicaciones")
    comentarios = relationship("Comments", back_populates="publicacion")
    likes = relationship("Likes", back_populates="publicacion")
    filtro = relationship("Filtros", back_populates="publicaciones")


# Tabla Comments
class Comments(Base):
    __tablename__ = "comments"

    IDcomments = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)  # Imagen opcional para el comentario
    fecha = Column(DateTime, default=datetime.utcnow)  # Fecha del comentario

    # Foreign Keys
    publicIDComment = Column(Integer, ForeignKey("publicaciones.IDpublic"), nullable=False)  # Relación con publicaciones
    userIDComment = Column(Integer, ForeignKey("users.IDuser"), nullable=False)  # Relación con el usuario

    # Relationships
    usuario = relationship("User", back_populates="comentarios")
    publicacion = relationship("Publicaciones", back_populates="comentarios")
    respuestas = relationship("AnswersComments", back_populates="comentario")
    likes = relationship("Likes", back_populates="comentario")


# Tabla AnswersComments
class AnswersComments(Base):
    __tablename__ = "answers_comments"

    IDanswer = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)  # Fecha de la respuesta

    # Foreign Keys
    commentIDAnswer = Column(Integer, ForeignKey("comments.IDcomments"), nullable=False)  # Relación con el comentario original
    userIDAnswer = Column(Integer, ForeignKey("users.IDuser"), nullable=False)  # Relación con el usuario que respondió

    # Relationships
    comentario = relationship("Comments", back_populates="respuestas")
    usuario = relationship("User", back_populates="respuestas")
    likes = relationship("Likes", back_populates="respuesta")
# Tabla Likes
class Likes(Base):
    __tablename__ = "likes"

    IDlike = Column(Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    userIDLike = Column(Integer, ForeignKey("users.IDuser"), nullable=False)  # Usuario que dio el like
    publicIDLike = Column(Integer, ForeignKey("publicaciones.IDpublic"), nullable=True)  # Publicación que recibió el like
    commentIDLike = Column(Integer, ForeignKey("comments.IDcomments"), nullable=True)  # Comentario que recibió el like
    answerIDLike = Column(Integer, ForeignKey("answers_comments.IDanswer"), nullable=True)  # Respuesta que recibió el like

    # Relationships
    usuario = relationship("User", back_populates="likes")
    publicacion = relationship("Publicaciones", back_populates="likes")
    comentario = relationship("Comments", back_populates="likes")
    respuesta = relationship("AnswersComments", back_populates="likes")


