from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Tabla User
class User(Base):
    __tablename__ = "users"

    IDuser = Column(Integer, primary_key=True, autoincrement=True)
    correo = Column(String(255), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)

    publicaciones = relationship("Publicaciones", back_populates="usuario")


# Tabla Comments
class Comments(Base):
    __tablename__ = "comments"

    IDcomments = Column(Integer, primary_key=True, autoincrement=True)
    contenido = Column(Text, nullable=False)

    publicaciones = relationship("Publicaciones", back_populates="comentario")

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