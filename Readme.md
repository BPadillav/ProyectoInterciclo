![Logo de la Universidad](logo.png)


# PRÁCTICA DE LABORATORIO

---

**CARRERA:** Computación  
**ASIGNATURA:** Computación Paralela  

**NRO. PRÁCTICA:** Proyecto Interciclo 

**TÍTULO PRÁCTICA:** UPSGlam una Plataforma Social de Imágenes con Convolución y Dockerización   

**OBJETIVO ALCANZADO:**  

El proyecto se desarrollo acerca de una plataforma social de imágenes que nos permiten integrar tecnologías avanzadas como PyCUDA para el procesamiento de imágenes mediante algoritmos de convolución personalizados. Se implementó una API robusta y dockerizada que soporta el flujo de datos entre la aplicación móvil y el servidor, permitiendo a los usuarios interactuar mediante publicaciones, comentarios y reacciones en un entorno optimizado y funcional.

---

## Estructura del Proyecto
Carpeta backend: Esta carpeta contiene todo el código relacionado con la API y el procesamiento en el servidor.

app: Directorio que incluye la configuración general y las rutas del proyecto.

__init__.py: Archivo de inicialización del módulo app.
config.py: Archivo donde se define la configuración del proyecto, como variables de entorno o configuraciones específicas.
routes.py: Archivo que contiene las rutas principales de la API.
En el directorio controllers se maneja la lógica de las rutas y controla las interacciones entre las solicitudes y los servicios.

1. comment_controller.py: Controlador para gestionar las operaciones relacionadas con los comentarios.
2. filtro_controller.py: Controlador que implementa las operaciones de los filtros de convolución sobre las imágenes.
3. like_controller.py: Controlador para manejar los "likes" en las publicaciones.
4. publicacion_controller.py: Controlador responsable de las operaciones relacionadas con las publicaciones.
5. user_controller.py: Controlador para gestionar las operaciones de usuarios, como registro y autenticación.
6. database: Carpeta donde se maneja la conexión con la base de datos y las definiciones de modelos.

config.py: Configuración de la base de datos, como la URL de conexión.
init_db.py: Archivo encargado de inicializar las tablas y relaciones en la base de datos.
models.py: Archivo donde se definen los modelos de datos utilizados en el proyecto, como usuarios, publicaciones, etc.

En el directorio services se coloca la lógica de negocio del proyecto, separando el procesamiento de datos de los controladores.

1. comment_service.py: Servicio encargado de la lógica relacionada con los comentarios.
2. filtro_service.py: Servicio que implementa la lógica de los filtros de convolución.
3. like_service.py: Servicio que gestiona la lógica de los "likes".
4. publicacion_service.py: Servicio para manejar las operaciones relacionadas con publicaciones.
5. user_service.py: Servicio encargado de la lógica de usuarios, como el manejo de autenticación o datos personales.
6. requirements.txt: Archivo que lista las dependencias necesarias para ejecutar el proyecto (bibliotecas de Python).

Archivos raíz del proyecto:

.env: Archivo donde se almacenan las variables de entorno necesarias para el funcionamiento del proyecto.
.gitignore: Archivo que especifica qué archivos o carpetas deben ser ignorados por Git, como __pycache__.
Dockerfile: Archivo utilizado para crear una imagen Docker del backend.
docker-compose.yml: Archivo de configuración para orquestar contenedores Docker, incluyendo la API y la base de datos.
cert.pem y key.pem: Certificados SSL/TLS para habilitar conexiones HTTPS seguras.
logo.png: Imagen utilizada en el proyecto, posiblemente como parte de los filtros personalizados.
run.py: Archivo principal para ejecutar el servidor backend.

Carpeta frontend: En esta carpeta se presenta la estructura correspondiente al proyecto Android generado con Capacitor, que incluye carpetas y archivos esenciales para la construcción y configuración de la aplicación. Dentro de app/src, se encuentran los paquetes para pruebas instrumentadas (androidTest) y unitarias (test), así como el código fuente principal de la aplicación (main) con el archivo MainActivity.java y los recursos definidos en res. Además, en el nivel superior se incluyen archivos de configuración como build.gradle, capacitor.build.gradle y el AndroidManifest.xml. La carpeta gradle/wrapper contiene las herramientas necesarias para la gestión de versiones y configuración de Gradle.


**Conclusiones:**  

En conclusión, este proyecto integró PyCUDA, Docker y desarrollo móvil para crear una plataforma social eficiente. La dockerización simplificó el despliegue y aseguró un entorno estable, mientras que los filtros personalizados añadieron creatividad y la interfaz móvil intuitiva garantizó una experiencia fluida, cumpliendo los objetivos funcionales y visuales.

**Recomendaciones:** 

- Se recomienda considerar implementar técnicas adicionales que optimicen el rendimiento de los algoritmos de convolución, especialmente en dispositivos con hardware más limitado.
- Reforzar la protección de la API utilizando autenticación con tokens y asegurando el cifrado de datos importantes.
- Realizar pruebas de carga que garanticen un buen rendimiento en entornos con muchos usuarios.