from flask import request, jsonify
from backend.database.init_db import get_db  # Asegúrate de importar get_db correctamente
from backend.database.models import User, Comments, Likes, Filtros, Publicaciones

def register_routes(app):
    """
    Registra todas las rutas de la aplicación Flask.

    Args:
        app (Flask): La instancia de la aplicación Flask.
    """
    @app.route('/')
    def home():
        return "Bienvenido a la API"

    @app.route('/status', methods=['GET'])
    def status():
        return {"status": "running", "message": "La API está funcionando correctamente"}, 200
    
    @app.route('/test', methods=['GET'])
    def test():
        return "Ruta de prueba exitosa"
    
    # METODOS POST
    @app.route('/create_user', methods=['POST'])
    def create_user():
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Verifica si ya existe un usuario con el correo
        existing_user = db.query(User).filter(User.correo == data['correo']).first()
        if existing_user:
            return jsonify({'message': 'El usuario ya existe'}), 400

        # Si no existe, crea un nuevo usuario
        new_user = User(correo=data['correo'], contraseña=data['contraseña'])
        db.add(new_user)
        db.commit()

        return jsonify({'message': 'Usuario creado exitosamente'}), 201

    @app.route('/create_comment', methods=['POST'])
    def create_comment():
        data = request.get_json()  # Obtén los datos enviados
        db = next(get_db())  # Obtén la sesión de base de datos

        if 'contenido' not in data:
            return jsonify({"message": "Faltan datos"}), 400

        comment = Comments(contenido=data['contenido'])  # Crea el comentario
        db.add(comment)
        db.commit()

        return jsonify({"message": "Comentario creado exitosamente"}), 201

    @app.route('/create_like', methods=['POST'])
    def create_like():
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        if 'nombrelike' not in data:
            return jsonify({"message": "Faltan datos"}), 400

        like = Likes(nombrelike=data['nombrelike'])
        db.add(like)
        db.commit()

        return jsonify({"message": "Like creado exitosamente"}), 201

    @app.route('/create_filtro', methods=['POST'])
    def create_filtro():
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        if 'nombreFiltro' not in data:
            return jsonify({"message": "Faltan datos"}), 400

        filtro = Filtros(nombreFiltro=data['nombreFiltro'])
        db.add(filtro)
        db.commit()

        return jsonify({"message": "Filtro creado exitosamente"}), 201

    @app.route('/create_publicacion', methods=['POST'])
    def create_publicacion():
        db = next(get_db())
        data = request.get_json()

        # Validar campos obligatorios
        if 'ruta' not in data or 'userPublicID' not in data:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Verificar la existencia del usuario
        usuario = db.query(User).filter_by(IDuser=data['userPublicID']).first()
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar la existencia de entidades relacionadas opcionales
        comentario = db.query(Comments).filter_by(IDcomments=data.get('comentPublicID')).first() if data.get('comentPublicID') else None
        like = db.query(Likes).filter_by(IDlike=data.get('likePublicID')).first() if data.get('likePublicID') else None
        filtro = db.query(Filtros).filter_by(IDfiltro=data.get('filtroPublicID')).first() if data.get('filtroPublicID') else None

        # Depuración: imprime los valores encontrados
        print("Comentario encontrado:", comentario)
        print("Like encontrado:", like)
        print("Filtro encontrado:", filtro)

        # Crear la publicación con las relaciones
        publicacion = Publicaciones(
            ruta=data['ruta'],
            userPublicID=data['userPublicID'],
            comentPublicID=comentario.IDcomments if comentario else None,
            likePublicID=like.IDlike if like else None,
            filtroPublicID=filtro.IDfiltro if filtro else None
        )

        db.add(publicacion)
        db.commit()

        return jsonify({"message": "Publicación creada exitosamente"}), 201



# METODOS GET

    @app.route('/list_users', methods=['GET'])
    def list_users():
        db = next(get_db())  # Obtener la sesión de base de datos
        users = db.query(User).all()  # Consulta para obtener todos los usuarios
        user_list = [{'IDuser': user.IDuser, 'correo': user.correo} for user in users]  # Crear una lista de usuarios
        return jsonify(user_list), 200

    @app.route('/list_comments', methods=['GET'])
    def list_comments():
        db = next(get_db())  # Obtener la sesión de base de datos
        comments = db.query(Comments).all()  # Consulta para obtener todos los comentarios
        comment_list = [{'IDcomments': comment.IDcomments, 'contenido': comment.contenido} for comment in comments]
        return jsonify(comment_list), 200

    @app.route('/list_likes', methods=['GET'])
    def list_likes():
        db = next(get_db())  # Obtener la sesión de base de datos
        likes = db.query(Likes).all()  # Consulta para obtener todos los likes
        like_list = [{'IDlike': like.IDlike, 'nombrelike': like.nombrelike} for like in likes]
        return jsonify(like_list), 200

    @app.route('/list_filtros', methods=['GET'])
    def list_filtros():
        db = next(get_db())  # Obtener la sesión de base de datos
        filtros = db.query(Filtros).all()  # Consulta para obtener todos los filtros
        filtro_list = [{'IDfiltro': filtro.IDfiltro, 'nombreFiltro': filtro.nombreFiltro} for filtro in filtros]
        return jsonify(filtro_list), 200

    @app.route('/list_publicaciones', methods=['GET'])
    def list_publicaciones():
        db = next(get_db())
        publicaciones = db.query(Publicaciones).all()

        publicacion_list = []
        for publicacion in publicaciones:
            comentario = db.query(Comments).filter_by(IDcomments=publicacion.comentPublicID).first()
            like = db.query(Likes).filter_by(IDlike=publicacion.likePublicID).first()
            filtro = db.query(Filtros).filter_by(IDfiltro=publicacion.filtroPublicID).first()

            publicacion_list.append({
                "IDpublic": publicacion.IDpublic,
                "ruta": publicacion.ruta,
                "userPublicID": publicacion.userPublicID,
                "comentPublicID": publicacion.comentPublicID,
                "comentario": comentario.contenido if comentario else None,
                "likePublicID": publicacion.likePublicID,
                "like": like.nombrelike if like else None,
                "filtroPublicID": publicacion.filtroPublicID,
                "filtro": filtro.nombreFiltro if filtro else None
            })

        return jsonify(publicacion_list)
