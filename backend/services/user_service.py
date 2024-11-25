from backend.database.models import User
from database.__init__ import db as session
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

DEFAULT_AVATAR = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

# Registrar usuario
def create_user(email, password, username, fullname,avatar=None):
    # Verifica si el usuario ya existe
    existing_user = session.query(User).filter(User.email == email).first()
    if existing_user:
        raise ValueError("El correo ya está registrado.")

    # Asignar avatar predeterminado si no se proporciona uno
    avatar = avatar or DEFAULT_AVATAR

    # Crear nuevo usuario
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, username = username, fullname = fullname, avatar=avatar)
    session.add(new_user)
    session.commit()
    return new_user

# Iniciar sesión
def login_user(email, password):
    user = session.query(User).filter(User.email == email).first()
    if not user or not check_password_hash(user.password, password):
        raise ValueError("Credenciales inválidas.")
    return user

# Obtener usuario por ID
def get_user_by_id(user_id):
    return session.query(User).filter(User.IDuser == user_id).first()

# Actualizar usuario
def update_user(user_id, email=None, password=None, avatar=None):
    user = session.query(User).filter(User.IDuser == user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado.")

    if email:
        user.email = email
    if password:
        user.password = generate_password_hash(password)
    if avatar:
        user.avatar = avatar

    session.commit()
    return user

# Eliminar usuario
def delete_user(user_id):
    user = session.query(User).filter(User.IDuser == user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado.")
    
    session.delete(user)
    session.commit()
    return True
