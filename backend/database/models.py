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


# Tabla Comments
class Comments(Base):
    __tablename__ = "comments"

    IDcomments = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)  # Imagen opcional para el comentario
    fecha = Column(DateTime, default=datetime.utcnow)  # Fecha del comentario
    likes = Column(Integer, default=0)  # Likes en el comentario

    publicaciones = relationship("Publicaciones", back_populates="comentario")
    respuestas = relationship("AnswersComments", back_populates="comentario")


# Tabla Likes
class Likes(Base):
    __tablename__ = "likes"

    IDlike = Column(Integer, primary_key=True, autoincrement=True)
    nombrelike = Column(String(255), nullable=False)

    publicaciones = relationship("Publicaciones", back_populates="like")


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
    ruta = Column(String(255), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Foreign Keys
    userPublicID = Column(Integer, ForeignKey("users.IDuser"), nullable=False)
    comentPublicID = Column(Integer, ForeignKey("comments.IDcomments"), nullable=True)
    likePublicID = Column(Integer, ForeignKey("likes.IDlike"), nullable=True)
    filtroPublicID = Column(Integer, ForeignKey("filtros.IDfiltro"), nullable=True)

    # Relationships
    usuario = relationship("User", back_populates="publicaciones")
    comentario = relationship("Comments", back_populates="publicaciones")
    like = relationship("Likes", back_populates="publicaciones")
    filtro = relationship("Filtros", back_populates="publicaciones")


# Tabla AnswersComments
class AnswersComments(Base):
    __tablename__ = "answers_comments"

    IDanswer = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)  # Fecha de la respuesta
    likes = Column(Integer, default=0)  # Likes en la respuesta
    commentID = Column(Integer, ForeignKey("comments.IDcomments"), nullable=False)

    comentario = relationship("Comments", back_populates="respuestas")
