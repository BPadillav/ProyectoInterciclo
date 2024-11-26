FROM nvidia/cuda:12.5.1-cudnn-devel-ubuntu20.04

# Establecer el directorio de trabajo
WORKDIR /app

# Actualizar el sistema e instalar Python y pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Asegúrate de que 'python' y 'pip' están enlazados correctamente
RUN [ ! -e /usr/bin/python ] && ln -s /usr/bin/python3 /usr/bin/python || echo "Python symlink already exists"
RUN [ ! -e /usr/bin/pip ] && ln -s /usr/bin/pip3 /usr/bin/pip || echo "Pip symlink already exists"

# Copiar el archivo de requerimientos
COPY ./backend/requirements.txt requirements.txt

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY ./backend /app/backend
COPY ./run.py /app/
COPY ./cert.pem /app/
COPY ./key.pem /app/

# Configurar la variable de entorno FLASK_APP
ENV FLASK_APP=run.py

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar Flask
CMD ["python", "run.py"]
