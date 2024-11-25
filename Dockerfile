FROM python:3.11-slim

WORKDIR /app

# Instala dependencias del sistema necesarias, incluyendo netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Copia el archivo de dependencias
COPY ./backend/requirements.txt requirements.txt

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del backend, el archivo principal y los certificados SSL
COPY ./backend /app/backend
COPY ./run.py /app/
COPY ./cert.pem /app/
COPY ./key.pem /app/

# Configurar FLASK_APP
ENV FLASK_APP=run.py

EXPOSE 5000

# Comando para ejecutar Flask
CMD ["python", "run.py"]
