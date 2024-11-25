from flask import request, jsonify
from backend.database.init_db import get_db  # Asegúrate de importar get_db correctamente
from backend.database.models import User, Comments, Likes, Filtros, Publicaciones, AnswersComments

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
        existing_user = db.query(User).filter(User.email == data['email']).first()
        if existing_user:
            return jsonify({'message': 'El usuario ya existe'}), 400

        # Si no existe, crea un nuevo usuario
        new_user = User(email=data['email'], password=data['password'], avatar=data.get('avatar'))
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
        user_list = [{'IDuser': user.IDuser, 'email': user.email} for user in users]  # Crear una lista de usuarios
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

#METODOS PUT

    @app.route('/update_user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el usuario a actualizar
        user = db.query(User).filter_by(IDuser=user_id).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Actualizar el correo y la contraseña si están presentes en los datos enviados
        if 'correo' in data:
            user.correo = data['correo']
        if 'contraseña' in data:
            user.contraseña = data['contraseña']

        db.commit()

        return jsonify({"message": "Usuario actualizado exitosamente"}), 200

    @app.route('/update_comment/<int:comment_id>', methods=['PUT'])
    def update_comment(comment_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el comentario a actualizar
        comment = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Actualizar el contenido del comentario
        if 'contenido' in data:
            comment.contenido = data['contenido']

        db.commit()

        return jsonify({"message": "Comentario actualizado exitosamente"}), 200

    @app.route('/update_like/<int:like_id>', methods=['PUT'])
    def update_like(like_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el like a actualizar
        like = db.query(Likes).filter_by(IDlike=like_id).first()
        if not like:
            return jsonify({"message": "Like no encontrado"}), 404

        # Actualizar el nombre del like
        if 'nombrelike' in data:
            like.nombrelike = data['nombrelike']

        db.commit()

        return jsonify({"message": "Like actualizado exitosamente"}), 200


    @app.route('/update_filtro/<int:filtro_id>', methods=['PUT'])
    def update_filtro(filtro_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el filtro a actualizar
        filtro = db.query(Filtros).filter_by(IDfiltro=filtro_id).first()
        if not filtro:
            return jsonify({"message": "Filtro no encontrado"}), 404

        # Actualizar el nombre del filtro
        if 'nombreFiltro' in data:
            filtro.nombreFiltro = data['nombreFiltro']

        db.commit()

        return jsonify({"message": "Filtro actualizado exitosamente"}), 200
    
    @app.route('/update_publicacion/<int:public_id>', methods=['PUT'])
    def update_publicacion(public_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar la publicación a actualizar
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        # Actualizar los campos si están presentes en los datos
        if 'ruta' in data:
            publicacion.ruta = data['ruta']
        
        if 'userPublicID' in data:
            publicacion.userPublicID = data['userPublicID']

        if 'comentPublicID' in data:
            comentario = db.query(Comments).filter_by(IDcomments=data['comentPublicID']).first()
            if comentario:
                publicacion.comentPublicID = comentario.IDcomments
            else:
                return jsonify({"message": "Comentario no encontrado"}), 404

        if 'likePublicID' in data:
            like = db.query(Likes).filter_by(IDlike=data['likePublicID']).first()
            if like:
                publicacion.likePublicID = like.IDlike
            else:
                return jsonify({"message": "Like no encontrado"}), 404

        if 'filtroPublicID' in data:
            filtro = db.query(Filtros).filter_by(IDfiltro=data['filtroPublicID']).first()
            if filtro:
                publicacion.filtroPublicID = filtro.IDfiltro
            else:
                return jsonify({"message": "Filtro no encontrado"}), 404

        db.commit()

        return jsonify({"message": "Publicación actualizada exitosamente"}), 200

#METODOS DELETE

    @app.route('/delete_user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el usuario a eliminar
        user = db.query(User).filter_by(IDuser=user_id).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        db.delete(user)
        db.commit()

        return jsonify({"message": "Usuario eliminado exitosamente"}), 200

    @app.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
    def delete_comment(comment_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el comentario a eliminar
        comment = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        db.delete(comment)
        db.commit()

        return jsonify({"message": "Comentario eliminado exitosamente"}), 200
    
    @app.route('/delete_like/<int:like_id>', methods=['DELETE'])
    def delete_like(like_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el like a eliminar
        like = db.query(Likes).filter_by(IDlike=like_id).first()
        if not like:
            return jsonify({"message": "Like no encontrado"}), 404

        db.delete(like)
        db.commit()

        return jsonify({"message": "Like eliminado exitosamente"}), 200
    
    @app.route('/delete_filtro/<int:filtro_id>', methods=['DELETE'])
    def delete_filtro(filtro_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el filtro a eliminar
        filtro = db.query(Filtros).filter_by(IDfiltro=filtro_id).first()
        if not filtro:
            return jsonify({"message": "Filtro no encontrado"}), 404

        db.delete(filtro)
        db.commit()

        return jsonify({"message": "Filtro eliminado exitosamente"}), 200
    
    @app.route('/delete_publicacion/<int:public_id>', methods=['DELETE'])
    def delete_publicacion(public_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar la publicación a eliminar
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        db.delete(publicacion)
        db.commit()

        return jsonify({"message": "Publicación eliminada exitosamente"}), 200


from flask import request, jsonify
from backend.database.init_db import get_db  # Asegúrate de importar get_db correctamente
from backend.database.models import User, Comments, Likes, Filtros, Publicaciones, AnswersComments

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
        existing_user = db.query(User).filter(User.email == data['email']).first()
        if existing_user:
            return jsonify({'message': 'El usuario ya existe'}), 400

        # Si no existe, crea un nuevo usuario
        new_user = User(email=data['email'], password=data['password'], avatar=data.get('avatar'))
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
        user_list = [{'IDuser': user.IDuser, 'email': user.email} for user in users]  # Crear una lista de usuarios
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

#METODOS PUT

    @app.route('/update_user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el usuario a actualizar
        user = db.query(User).filter_by(IDuser=user_id).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Actualizar el correo y la contraseña si están presentes en los datos enviados
        if 'correo' in data:
            user.correo = data['correo']
        if 'contraseña' in data:
            user.contraseña = data['contraseña']

        db.commit()

        return jsonify({"message": "Usuario actualizado exitosamente"}), 200

    @app.route('/update_comment/<int:comment_id>', methods=['PUT'])
    def update_comment(comment_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el comentario a actualizar
        comment = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Actualizar el contenido del comentario
        if 'contenido' in data:
            comment.contenido = data['contenido']

        db.commit()

        return jsonify({"message": "Comentario actualizado exitosamente"}), 200

    @app.route('/update_like/<int:like_id>', methods=['PUT'])
    def update_like(like_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el like a actualizar
        like = db.query(Likes).filter_by(IDlike=like_id).first()
        if not like:
            return jsonify({"message": "Like no encontrado"}), 404

        # Actualizar el nombre del like
        if 'nombrelike' in data:
            like.nombrelike = data['nombrelike']

        db.commit()

        return jsonify({"message": "Like actualizado exitosamente"}), 200


    @app.route('/update_filtro/<int:filtro_id>', methods=['PUT'])
    def update_filtro(filtro_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el filtro a actualizar
        filtro = db.query(Filtros).filter_by(IDfiltro=filtro_id).first()
        if not filtro:
            return jsonify({"message": "Filtro no encontrado"}), 404

        # Actualizar el nombre del filtro
        if 'nombreFiltro' in data:
            filtro.nombreFiltro = data['nombreFiltro']

        db.commit()

        return jsonify({"message": "Filtro actualizado exitosamente"}), 200
    
    @app.route('/update_publicacion/<int:public_id>', methods=['PUT'])
    def update_publicacion(public_id):
        data = request.get_json()
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar la publicación a actualizar
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        # Actualizar los campos si están presentes en los datos
        if 'ruta' in data:
            publicacion.ruta = data['ruta']
        
        if 'userPublicID' in data:
            publicacion.userPublicID = data['userPublicID']

        if 'comentPublicID' in data:
            comentario = db.query(Comments).filter_by(IDcomments=data['comentPublicID']).first()
            if comentario:
                publicacion.comentPublicID = comentario.IDcomments
            else:
                return jsonify({"message": "Comentario no encontrado"}), 404

        if 'likePublicID' in data:
            like = db.query(Likes).filter_by(IDlike=data['likePublicID']).first()
            if like:
                publicacion.likePublicID = like.IDlike
            else:
                return jsonify({"message": "Like no encontrado"}), 404

        if 'filtroPublicID' in data:
            filtro = db.query(Filtros).filter_by(IDfiltro=data['filtroPublicID']).first()
            if filtro:
                publicacion.filtroPublicID = filtro.IDfiltro
            else:
                return jsonify({"message": "Filtro no encontrado"}), 404

        db.commit()

        return jsonify({"message": "Publicación actualizada exitosamente"}), 200

#METODOS DELETE

    @app.route('/delete_user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el usuario a eliminar
        user = db.query(User).filter_by(IDuser=user_id).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        db.delete(user)
        db.commit()

        return jsonify({"message": "Usuario eliminado exitosamente"}), 200

    @app.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
    def delete_comment(comment_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el comentario a eliminar
        comment = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        db.delete(comment)
        db.commit()

        return jsonify({"message": "Comentario eliminado exitosamente"}), 200
    
    @app.route('/delete_like/<int:like_id>', methods=['DELETE'])
    def delete_like(like_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el like a eliminar
        like = db.query(Likes).filter_by(IDlike=like_id).first()
        if not like:
            return jsonify({"message": "Like no encontrado"}), 404

        db.delete(like)
        db.commit()

        return jsonify({"message": "Like eliminado exitosamente"}), 200
    
    @app.route('/delete_filtro/<int:filtro_id>', methods=['DELETE'])
    def delete_filtro(filtro_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar el filtro a eliminar
        filtro = db.query(Filtros).filter_by(IDfiltro=filtro_id).first()
        if not filtro:
            return jsonify({"message": "Filtro no encontrado"}), 404

        db.delete(filtro)
        db.commit()

        return jsonify({"message": "Filtro eliminado exitosamente"}), 200
    
    @app.route('/delete_publicacion/<int:public_id>', methods=['DELETE'])
    def delete_publicacion(public_id):
        db = next(get_db())  # Obtén la sesión de base de datos

        # Buscar la publicación a eliminar
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        db.delete(publicacion)
        db.commit()

        return jsonify({"message": "Publicación eliminada exitosamente"}), 200


    @app.route('/create_answer', methods=['POST'])
    def create_answer():
        """
        Crear una respuesta asociada a un comentario.
        """
        data = request.get_json()  # Obtén los datos enviados
        db = next(get_db())  # Obtén la sesión de base de datos

        if 'commentID' not in data or 'contenido' not in data:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Verifica si el comentario existe
        comment = db.query(Comments).filter_by(IDcomments=data['commentID']).first()
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Crea la respuesta
        answer = AnswersComments(
            contenido=data['contenido'],
            commentID=data['commentID'],
            likes=data.get('likes', 0)  # Si no se envían likes, se establece en 0
        )
        db.add(answer)
        db.commit()

        return jsonify({"message": "Respuesta creada exitosamente"}), 201


    @app.route('/list_answers/<int:comment_id>', methods=['GET'])
    def list_answers(comment_id):
        """
        Listar las respuestas asociadas a un comentario.
        """
        db = next(get_db())  # Obtén la sesión de base de datos

        # Verifica si el comentario existe
        comment = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comment:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Obtiene las respuestas asociadas al comentario
        answers = db.query(AnswersComments).filter_by(commentID=comment_id).all()
        answer_list = [
            {
                "IDanswer": answer.IDanswer,
                "contenido": answer.contenido,
                "fecha": answer.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "likes": answer.likes,
                "commentID": answer.commentID,
            }
            for answer in answers
        ]

        return jsonify(answer_list), 200


    @app.route('/update_answer/<int:answer_id>', methods=['PUT'])
    def update_answer(answer_id):
        """
        Actualizar una respuesta existente.
        """
        data = request.get_json()  # Obtén los datos enviados
        db = next(get_db())  # Obtén la sesión de base de datos

        # Verifica si la respuesta existe
        answer = db.query(AnswersComments).filter_by(IDanswer=answer_id).first()
        if not answer:
            return jsonify({"message": "Respuesta no encontrada"}), 404

        # Actualiza los campos si están presentes en los datos
        if 'contenido' in data:
            answer.contenido = data['contenido']
        if 'likes' in data:
            answer.likes = data['likes']

        db.commit()

        return jsonify({"message": "Respuesta actualizada exitosamente"}), 200


    @app.route('/delete_answer/<int:answer_id>', methods=['DELETE'])
    def delete_answer(answer_id):
        """
        Eliminar una respuesta por su ID.
        """
        db = next(get_db())  # Obtén la sesión de base de datos

        # Verifica si la respuesta existe
        answer = db.query(AnswersComments).filter_by(IDanswer=answer_id).first()
        if not answer:
            return jsonify({"message": "Respuesta no encontrada"}), 404

        db.delete(answer)
        db.commit()

        return jsonify({"message": "Respuesta eliminada exitosamente"}), 200
