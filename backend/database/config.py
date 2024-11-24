import os
from dotenv import load_dotenv

# Carga las variables de entorno desde .env
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:1234@localhost:3306/instagram")
