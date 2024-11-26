from flask import request, jsonify, send_from_directory
from backend.database.init_db import get_db  # Asegúrate de importar get_db correctamente
from backend.database.models import User, Comments, Likes, Filtros, Publicaciones, AnswersComments
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
import os

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
    #usuarios
    @app.route('/create_user', methods=['POST'])
    def create_user():
        """
        Crear un nuevo usuario.
        """
        data = request.get_json()  # Obtiene los datos JSON del cuerpo de la solicitud
        db = next(get_db())  # Obtiene la sesión de la base de datos

        # Verifica si los campos requeridos están presentes
        if not data.get('email') or not data.get('username') or not data.get('password'):
            return jsonify({'valid': 'false','message': 'Correo electrónico, nombre de usuario y contraseña son requeridos'}), 400

        # Verifica si ya existe un usuario con el correo proporcionado
        existing_user = db.query(User).filter(User.email == data['email']).first()
        if existing_user:
            return jsonify({'valid': 'false','message': 'El usuario ya existe'}), 400

        # Verifica si ya existe un usuario con el nombre de usuario
        existing_username = db.query(User).filter(User.username == data['username']).first()
        if existing_username:
            return jsonify({'valid': 'false','message': 'El nombre de usuario ya existe'}), 400

        # Crear un nuevo usuario
        new_user = User(
            email=data['email'],
            username=data['username'],  # Añadido el campo 'username'
            fullname=data['fullname'],  # Añadido el campo 'fullname'
            password=data['password'],
            avatar=data.get('avatar')  # Opcional
        )
        db.add(new_user)
        db.commit()

        return jsonify({'valid': 'true','message': 'Usuario creado exitosamente', 'user_id': new_user.IDuser}), 201


    @app.route('/update_user/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        """
        Actualizar los datos de un usuario.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el usuario
        user = db.query(User).filter_by(IDuser=user_id).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Actualizar campos según los datos enviados
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        if 'avatar' in data:
            user.avatar = data['avatar']

        db.commit()

        return jsonify({"message": "Usuario actualizado exitosamente"}), 200
    
    @app.route('/delete_user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """
        Eliminar un usuario por su ID.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el usuario
        user = db.query(User).filter_by(IDuser=user_id).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Eliminar el usuario
        db.delete(user)
        db.commit()

        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    
    @app.route('/list_users', methods=['GET'])
    def list_users():
        """
        Listar todos los usuarios.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos
        users = db.query(User).all()  # Consulta para obtener todos los usuarios

        # Crear una lista de usuarios para la respuesta
        user_list = [
            {
                "IDuser": user.IDuser,
                "email": user.email,
                "avatar": user.avatar
            }
            for user in users
        ]

        return jsonify(user_list), 200

    @app.route('/users/login', methods=['POST'])
    def login():
        """
        Permite a un usuario iniciar sesión.
        """
        data = request.get_json()  # Obtiene los datos JSON del cuerpo de la solicitud
        db = next(get_db())  # Obtiene la sesión de la base de datos

        # Verifica si los campos requeridos están presentes
        if not data.get('email') or not data.get('password'):
            return jsonify({'valid': 'false', 'message': 'Correo electrónico y contraseña son requeridos'}), 400

        # Buscar al usuario en la base de datos
        user = db.query(User).filter(User.email == data['email']).first()
        if not user:
            return jsonify({'valid': 'false', 'message': 'Credenciales incorrectas'}), 200

        # Verifica la contraseña directamente
        if user.password != data['password']:
            return jsonify({'valid': 'false', 'message': 'Credenciales incorrectas'}), 200

        # Retorna los datos del usuario si las credenciales son correctas
        return jsonify({
            "valid": 'true',
            "IDuser": user.IDuser,
            "email": user.email,
            "username": user.username,
            "fullname": user.fullname,
            "avatar": user.avatar
        }), 200




#FILTROS******************************************************************

    @app.route('/create_filtro', methods=['POST'])
    def create_filtro():
        """
        Crear un nuevo filtro.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Validar que los datos necesarios estén presentes
        if 'nombreFiltro' not in data:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Crear el filtro
        filtro = Filtros(nombreFiltro=data['nombreFiltro'])
        db.add(filtro)
        db.commit()

        return jsonify({"message": "Filtro creado exitosamente", "filtro_id": filtro.IDfiltro}), 201



    @app.route('/list_filtros', methods=['GET'])
    def list_filtros():
        """
        Obtener una lista de todos los filtros.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos
        filtros = db.query(Filtros).all()

        # Estructura de salida
        filtro_list = [{'IDfiltro': filtro.IDfiltro, 'nombreFiltro': filtro.nombreFiltro} for filtro in filtros]
        return jsonify(filtro_list), 200


    @app.route('/update_filtro/<int:filtro_id>', methods=['PUT'])
    def update_filtro(filtro_id):
        """
        Actualizar un filtro por su ID.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el filtro
        filtro = db.query(Filtros).filter_by(IDfiltro=filtro_id).first()
        if not filtro:
            return jsonify({"message": "Filtro no encontrado"}), 404

        # Actualizar el nombre del filtro
        if 'nombreFiltro' in data:
            filtro.nombreFiltro = data['nombreFiltro']

        db.commit()

        return jsonify({"message": "Filtro actualizado exitosamente"}), 200


    @app.route('/delete_filtro/<int:filtro_id>', methods=['DELETE'])
    def delete_filtro(filtro_id):
        """
        Eliminar un filtro por su ID.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el filtro
        filtro = db.query(Filtros).filter_by(IDfiltro=filtro_id).first()
        if not filtro:
            return jsonify({"message": "Filtro no encontrado"}), 404

        # Eliminar el filtro
        db.delete(filtro)
        db.commit()

        return jsonify({"message": "Filtro eliminado exitosamente"}), 200



#PUBLICACIONES*****************************************************

    @app.route('/uploads/<path:filename>', methods=['GET'])
    def uploaded_file(filename):
        """
        Sirve los archivos desde el directorio de subidas.
        """
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/create_publicacion', methods=['POST'])
    def create_publicacion():
        """
        Crear una nueva publicación con una foto subida como archivo.
        """
        from datetime import datetime

        # Datos del formulario
        userIDPublic = request.form.get('userIDPublic')
        contenido = request.form.get('contenido', '')
        filtroIDPublic = request.form.get('filtroIDPublic', None)
        file = request.files.get('rutaImagen')

        # Validaciones básicas
        if not userIDPublic or not file:
            return jsonify({"message": "Datos obligatorios faltantes."}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Formato de archivo no permitido."}), 400

        try:
            db = next(get_db())  # Obtén la sesión de la base de datos

            # Validar usuario
            usuario = db.query(User).filter_by(IDuser=userIDPublic).first()
            if not usuario:
                return jsonify({"message": "Usuario no encontrado."}), 404

            # Validar filtro
            filtro = db.query(Filtros).filter_by(IDfiltro=filtroIDPublic).first() if filtroIDPublic else None
            if filtroIDPublic and not filtro:
                return jsonify({"message": f"El filtro con ID {filtroIDPublic} no existe."}), 400

            # Crear la publicación sin guardar la imagen todavía
            nueva_publicacion = Publicaciones(
                rutaImagen="",  # Temporalmente vacío
                contenido=contenido,
                userIDPublic=userIDPublic,
                filtroIDPublic=filtroIDPublic if filtro else None,
                fecha=datetime.utcnow()
            )
            db.add(nueva_publicacion)
            db.flush()  # Esto genera el ID de la publicación sin hacer commit aún

            # Ahora que tenemos el ID, guardar el archivo con el ID de la publicación
            filename = secure_filename(f"post_{nueva_publicacion.IDpublic}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Actualizar la ruta de la imagen en la publicación
            nueva_publicacion.rutaImagen = filepath
            db.commit()  # Ahora hacemos commit con la ruta de la imagen actualizada

            return jsonify({
                "message": "Publicación creada exitosamente",
                "publicacion": {
                    "id": nueva_publicacion.IDpublic,
                    "rutaImagen": nueva_publicacion.rutaImagen,
                    "contenido": nueva_publicacion.contenido,
                    "userIDPublic": nueva_publicacion.userIDPublic,
                    "filtroIDPublic": nueva_publicacion.filtroIDPublic,
                    "fecha": nueva_publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                }
            }), 201
        except Exception as e:
            return jsonify({"message": f"Error al procesar la publicación: {str(e)}"}), 500







    @app.route('/list_publicaciones', methods=['GET'])
    def list_publicaciones():
        """
        Listar todas las publicaciones con detalles de usuario y filtro.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos
        publicaciones = db.query(Publicaciones).all()

        # print('a',publicaciones)

        # Estructura de salida
        publicacion_list = [
            {
                "id": publicacion.IDpublic,
                "username": publicacion.usuario.username,
                "avatar": publicacion.rutaImagen,
                "image": publicacion.rutaImagen,
                "likes": 0,
                "content": publicacion.contenido,
                "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "userIDPublic": publicacion.userIDPublic,
                "filtroIDPublic": publicacion.filtroIDPublic,
                "filtro": publicacion.filtro.nombreFiltro if publicacion.filtro else None,
            }
            for publicacion in publicaciones
        ]

        return jsonify(publicacion_list), 200


    @app.route('/update_publicacion/<int:public_id>', methods=['PUT'])
    def update_publicacion(public_id):
        """
        Actualizar una publicación por su ID.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar la publicación
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        # Actualizar los campos si están presentes
        if 'rutaImagen' in data:
            publicacion.rutaImagen = data['rutaImagen']
        if 'contenido' in data:
            publicacion.contenido = data['contenido']
        if 'filtroIDPublic' in data:
            filtro = db.query(Filtros).filter_by(IDfiltro=data['filtroIDPublic']).first()
            if filtro:
                publicacion.filtroIDPublic = filtro.IDfiltro
            else:
                return jsonify({"message": "Filtro no encontrado"}), 404

        db.commit()

        return jsonify({"message": "Publicación actualizada exitosamente"}), 200


    @app.route('/delete_publicacion/<int:public_id>', methods=['DELETE'])
    def delete_publicacion(public_id):
        """
        Eliminar una publicación por su ID.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar la publicación
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        # Eliminar la publicación
        db.delete(publicacion)
        db.commit()

        return jsonify({"message": "Publicación eliminada exitosamente"}), 200


#COMMENTS********************************************************************************
    @app.route('/create_comment', methods=['POST'])
    def create_comment():
        """
        Crear un nuevo comentario.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Validar datos obligatorios
        if 'contenido' not in data or 'publicIDComment' not in data or 'userIDComment' not in data:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Verificar la existencia de la publicación
        publicacion = db.query(Publicaciones).filter_by(IDpublic=data['publicIDComment']).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        # Verificar la existencia del usuario
        usuario = db.query(User).filter_by(IDuser=data['userIDComment']).first()
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Crear el comentario
        comentario = Comments(
            contenido=data['contenido'],
            image=data.get('image'),
            publicIDComment=data['publicIDComment'],
            userIDComment=data['userIDComment']
        )
        db.add(comentario)
        db.commit()

        return jsonify({"message": "Comentario creado exitosamente", "comment_id": comentario.IDcomments}), 201

    @app.route('/list_comments', methods=['GET'])
    def list_comments():
        """
        Listar todos los comentarios con detalles de publicación y usuario.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos
        comentarios = db.query(Comments).all()

        # Estructura de salida
        comment_list = [
            {
                "IDcomments": comment.IDcomments,
                "contenido": comment.contenido,
                "image": comment.image,
                "fecha": comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "publicIDComment": comment.publicIDComment,
                "publicacion": comment.publicacion.rutaImagen if comment.publicacion else None,
                "userIDComment": comment.userIDComment,
                "usuario": comment.usuario.email if comment.usuario else None
            }
            for comment in comentarios
        ]

        return jsonify(comment_list), 200
    
    @app.route('/list_comments/<int:publication_id>', methods=['GET'])
    def list_comments_by_publication(publication_id):
        """
        Listar comentarios de una publicación específica con detalles de usuario.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Filtrar comentarios por el ID de publicación
        comentarios = db.query(Comments).filter(Comments.publicIDComment == publication_id).all()

        # Estructura de salida
        comment_list = [
            {
                "IDcomments": comment.IDcomments,
                "contenido": comment.contenido,
                "image": comment.image,
                "fecha": comment.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "publicIDComment": comment.publicIDComment,
                "publicacion": comment.publicacion.rutaImagen if comment.publicacion else None,
                "userIDComment": comment.userIDComment,
                "usuario": comment.usuario.email if comment.usuario else None
            }
            for comment in comentarios
        ]

        # Devuelve la lista de comentarios filtrados
        return jsonify(comment_list), 200



    @app.route('/update_comment/<int:comment_id>', methods=['PUT'])
    def update_comment(comment_id):
        """
        Actualizar un comentario por su ID.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el comentario
        comentario = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Actualizar los campos si están presentes
        if 'contenido' in data:
            comentario.contenido = data['contenido']
        if 'image' in data:
            comentario.image = data['image']

        db.commit()

        return jsonify({"message": "Comentario actualizado exitosamente"}), 200


    @app.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
    def delete_comment(comment_id):
        """
        Eliminar un comentario por su ID.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el comentario
        comentario = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Eliminar el comentario
        db.delete(comentario)
        db.commit()

        return jsonify({"message": "Comentario eliminado exitosamente"}), 200




#ANSWER******************************************

    @app.route('/create_answer', methods=['POST'])
    def create_answer():
        """
        Crear una nueva respuesta asociada a un comentario.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Validar datos obligatorios
        if 'commentIDAnswer' not in data or 'contenido' not in data or 'userIDAnswer' not in data:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Verificar si el comentario existe
        comentario = db.query(Comments).filter_by(IDcomments=data['commentIDAnswer']).first()
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Verificar si el usuario existe
        usuario = db.query(User).filter_by(IDuser=data['userIDAnswer']).first()
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Crear la respuesta
        respuesta = AnswersComments(
            contenido=data['contenido'],
            commentIDAnswer=data['commentIDAnswer'],
            userIDAnswer=data['userIDAnswer']
        )
        db.add(respuesta)
        db.commit()

        return jsonify({"message": "Respuesta creada exitosamente", "answer_id": respuesta.IDanswer}), 201



    @app.route('/list_answers/<int:comment_id>', methods=['GET'])
    def list_answers(comment_id):
        """
        Listar todas las respuestas asociadas a un comentario.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Verificar si el comentario existe
        comentario = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Obtener las respuestas asociadas al comentario
        respuestas = db.query(AnswersComments).filter_by(commentIDAnswer=comment_id).all()

        # Estructura de salida
        answer_list = [
            {
                "IDanswer": respuesta.IDanswer,
                "contenido": respuesta.contenido,
                "fecha": respuesta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "commentIDAnswer": respuesta.commentIDAnswer,
                "userIDAnswer": respuesta.userIDAnswer,
                "usuario": respuesta.usuario.email if respuesta.usuario else None
            }
            for respuesta in respuestas
        ]

        return jsonify(answer_list), 200

    @app.route('/update_answer/<int:answer_id>', methods=['PUT'])
    def update_answer(answer_id):
        """
        Actualizar una respuesta por su ID.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar la respuesta
        respuesta = db.query(AnswersComments).filter_by(IDanswer=answer_id).first()
        if not respuesta:
            return jsonify({"message": "Respuesta no encontrada"}), 404

        # Actualizar los campos si están presentes
        if 'contenido' in data:
            respuesta.contenido = data['contenido']

        db.commit()

        return jsonify({"message": "Respuesta actualizada exitosamente"}), 200

    @app.route('/delete_answer/<int:answer_id>', methods=['DELETE'])
    def delete_answer(answer_id):
        """
        Eliminar una respuesta por su ID.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar la respuesta
        respuesta = db.query(AnswersComments).filter_by(IDanswer=answer_id).first()
        if not respuesta:
            return jsonify({"message": "Respuesta no encontrada"}), 404

        # Eliminar la respuesta
        db.delete(respuesta)
        db.commit()

        return jsonify({"message": "Respuesta eliminada exitosamente"}), 200


    @app.route('/list_answers_by_comment/<int:comment_id>', methods=['GET'])
    def list_answers_by_comment(comment_id):
        """
        Listar todas las respuestas asociadas a un comentario específico.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Verificar si el comentario existe
        comentario = db.query(Comments).filter_by(IDcomments=comment_id).first()
        if not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404

        # Obtener las respuestas asociadas al comentario
        respuestas = db.query(AnswersComments).filter_by(commentIDAnswer=comment_id).all()

        # Estructura de salida
        answer_list = [
            {
                "IDanswer": respuesta.IDanswer,
                "contenido": respuesta.contenido,
                "fecha": respuesta.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "likes": respuesta.likes,
                "commentIDAnswer": respuesta.commentIDAnswer,
                "userIDAnswer": respuesta.userIDAnswer
            }
            for respuesta in respuestas
        ]

        return jsonify(answer_list), 200


# LIKES ******************************************************************

    @app.route('/create_like', methods=['POST'])
    def create_like():
        """
        Crear un nuevo like asociado a una publicación, comentario o respuesta.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Validar que los datos necesarios estén presentes
        if not any(key in data for key in ['publicIDLike', 'commentIDLike', 'answerIDLike']) or 'userIDLike' not in data:
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Verificar la existencia del usuario
        usuario = db.query(User).filter_by(IDuser=data['userIDLike']).first()
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar si la publicación, comentario o respuesta existen
        publicacion = db.query(Publicaciones).filter_by(IDpublic=data.get('publicIDLike')).first() if data.get('publicIDLike') else None
        comentario = db.query(Comments).filter_by(IDcomments=data.get('commentIDLike')).first() if data.get('commentIDLike') else None
        respuesta = db.query(AnswersComments).filter_by(IDanswer=data.get('answerIDLike')).first() if data.get('answerIDLike') else None

        if data.get('publicIDLike') and not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404
        if data.get('commentIDLike') and not comentario:
            return jsonify({"message": "Comentario no encontrado"}), 404
        if data.get('answerIDLike') and not respuesta:
            return jsonify({"message": "Respuesta no encontrada"}), 404

        # Crear el like
        like = Likes(
            userIDLike=data['userIDLike'],
            publicIDLike=data.get('publicIDLike'),
            commentIDLike=data.get('commentIDLike'),
            answerIDLike=data.get('answerIDLike')
        )
        db.add(like)
        db.commit()

        return jsonify({"message": "Like creado exitosamente", "like_id": like.IDlike}), 201


    @app.route('/list_likes', methods=['GET'])
    def list_likes():
        """
        Listar todos los likes con detalles de usuario, publicación, comentario y respuesta.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos
        likes = db.query(Likes).all()

        # Estructura de salida
        like_list = [
            {
                "IDlike": like.IDlike,
                "userIDLike": like.userIDLike,
                "usuario": like.usuario.email if like.usuario else None,
                "publicIDLike": like.publicIDLike,
                "publicacion": like.publicacion.rutaImagen if like.publicacion else None,
                "commentIDLike": like.commentIDLike,
                "comentario": like.comentario.contenido if like.comentario else None,
                "answerIDLike": like.answerIDLike,
                "respuesta": like.respuesta.contenido if like.respuesta else None
            }
            for like in likes
        ]

        return jsonify(like_list), 200


    @app.route('/update_like/<int:like_id>', methods=['PUT'])
    def update_like(like_id):
        """
        Actualizar un like por su ID.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el like
        like = db.query(Likes).filter_by(IDlike=like_id).first()
        if not like:
            return jsonify({"message": "Like no encontrado"}), 404

        # Actualizar los campos si están presentes
        if 'publicIDLike' in data:
            publicacion = db.query(Publicaciones).filter_by(IDpublic=data['publicIDLike']).first()
            if publicacion:
                like.publicIDLike = publicacion.IDpublic
            else:
                return jsonify({"message": "Publicación no encontrada"}), 404

        if 'commentIDLike' in data:
            comentario = db.query(Comments).filter_by(IDcomments=data['commentIDLike']).first()
            if comentario:
                like.commentIDLike = comentario.IDcomments
            else:
                return jsonify({"message": "Comentario no encontrado"}), 404

        if 'answerIDLike' in data:
            respuesta = db.query(AnswersComments).filter_by(IDanswer=data['answerIDLike']).first()
            if respuesta:
                like.answerIDLike = respuesta.IDanswer
            else:
                return jsonify({"message": "Respuesta no encontrada"}), 404

        db.commit()

        return jsonify({"message": "Like actualizado exitosamente"}), 200


    @app.route('/delete_like/<int:like_id>', methods=['DELETE'])
    def delete_like(like_id):
        """
        Eliminar un like por su ID.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Buscar el like
        like = db.query(Likes).filter_by(IDlike=like_id).first()
        if not like:
            return jsonify({"message": "Like no encontrado"}), 404

        # Eliminar el like
        db.delete(like)
        db.commit()

        return jsonify({"message": "Like eliminado exitosamente"}), 200

# FILTROS CUDA ******************************************************************

    from backend.filters import process_image, allowed_file

    @app.route('/apply_filter', methods=['POST'])
    def apply_filter():
        """
        Aplica un filtro a una imagen enviada en Base64 y devuelve la URL de la imagen procesada.
        """
        try:
            from datetime import datetime
            import base64
            import os
            import cv2
            import numpy as np

            # Filtros estáticos disponibles
            available_filters = {
                "sharpen": "Filtro de nitidez",
                "dilation": "Filtro de dilatación",
                "canny": "Filtro Canny"
            }

            # Parámetros recibidos del cliente
            filter_type = request.form.get('filter_type', 'sharpen')
            num_threads = int(request.form.get('num_threads', 1024))
            mask_size = int(request.form.get('mask_size', 3))
            base64_image = request.form.get('rutaImagen')

            # Validar filtro seleccionado
            if filter_type not in available_filters:
                return jsonify({"message": "Filtro no válido."}), 400

            # Validar imagen en Base64
            if not base64_image:
                return jsonify({"message": "Imagen en Base64 no proporcionada."}), 400

            # Decodificar la imagen Base64
            header, encoded = base64_image.split(',', 1)
            image_data = base64.b64decode(encoded)
            np_img = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            if image is None:
                return jsonify({"message": "No se pudo leer la imagen proporcionada."}), 400

            # Procesar la imagen con el filtro seleccionado
            processed_image, time_results = process_image(num_threads, filter_type, mask_size, image)

            # Generar un nombre único para la imagen procesada
            filename = f"filtered_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Guardar la imagen procesada
            cv2.imwrite(filepath, processed_image)

            # Retornar la URL de la imagen procesada
            return jsonify({
                "message": "Filtro aplicado correctamente.",
                "processed_image_url": filename,
                "processing_time": time_results
            }), 200

        except Exception as e:
            return jsonify({"message": f"Error al aplicar filtro: {str(e)}"}), 500

