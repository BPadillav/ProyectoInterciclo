class Config:
    """
    Configuración de la aplicación Flask.
    """
    SECRET_KEY = "tu_clave_secreta_segura"  # Cambia esto por una clave más segura
    DEBUG = True  # Cambiar a False en producción
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@mysql:3306/instagram"
    SQLALCHEMY_TRACK_MODIFICATIONS = False