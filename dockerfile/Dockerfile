FROM python:3.11-slim

WORKDIR /app

# Copia el archivo de dependencias
COPY ./backend/requirements.txt requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio backend al contenedor
COPY ./backend /app/backend

EXPOSE 5000

# Ajusta el comando CMD para Flask
CMD ["python", "-m", "backend.app"]
