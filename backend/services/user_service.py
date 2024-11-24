from backend.database.models import User
from database.__init__ import db as session
from werkzeug.security import generate_password_hash, check_password_hash

# Registrar usuario
def create_user(email, password):
    # Verifica si el usuario ya existe
    existing_user = session.query(User).filter(User.correo == email).first()
    if existing_user:
        raise ValueError("El correo ya está registrado.")

    # Encripta la contraseña
    hashed_password = generate_password_hash(password)
    new_user = User(correo=email, contraseña=hashed_password)
    session.add(new_user)
    session.commit()
    return new_user

# Iniciar sesión
def login_user(email, password):
    # Verifica si el usuario existe
    user = session.query(User).filter(User.correo == email).first()
    if not user or not check_password_hash(user.contraseña, password):
        raise ValueError("Credenciales inválidas.")
    return user

# Obtener usuario por ID
def get_user_by_id(user_id):
    return session.query(User).filter(User.IDuser == user_id).first()

# Actualizar usuario
def update_user(user_id, email=None, password=None):
    user = session.query(User).filter(User.IDuser == user_id).first()
    if not user:
        raise ValueError("Usuario no encontrado.")

    if email:
        user.correo = email
    if password:
        user.contraseña = generate_password_hash(password)

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
