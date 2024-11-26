from flask import request, jsonify
from backend.database.init_db import get_db  # Asegúrate de importar get_db correctamente
from backend.database.models import User, Comments, Likes, Filtros, Publicaciones, AnswersComments
from sqlalchemy.orm import joinedload
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
            return jsonify({'message': 'Correo electrónico, nombre de usuario y contraseña son requeridos'}), 400

        # Verifica si ya existe un usuario con el correo proporcionado
        existing_user = db.query(User).filter(User.email == data['email']).first()
        if existing_user:
            return jsonify({'message': 'El usuario ya existe'}), 400

        # Verifica si ya existe un usuario con el nombre de usuario
        existing_username = db.query(User).filter(User.username == data['username']).first()
        if existing_username:
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400

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

        return jsonify({'message': 'Usuario creado exitosamente', 'user_id': new_user.IDuser}), 201


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
            return jsonify({'message': 'Correo electrónico y contraseña son requeridos'}), 400

        # Buscar al usuario en la base de datos
        user = db.query(User).filter(User.email == data['email']).first()
        if not user:
            return jsonify({'message': 'Credenciales incorrectas'}), 200

        # Verifica la contraseña directamente
        if user.password != data['password']:
            return jsonify({'message': 'Credenciales incorrectas'}), 200

        # Retorna los datos del usuario si las credenciales son correctas
        return jsonify({
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
 


# PUBLICACIONES *****************************************************

    @app.route('/create_publicacion', methods=['POST'])
    def create_publicacion():
        """
        Crear una nueva publicación.
        """
        data = request.get_json()
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Validar datos obligatorios
        if 'userIDPublic' not in data:
            return jsonify({"message": "Faltan datos obligatorios: userIDPublic"}), 400

        # Verificar la existencia del usuario
        usuario = db.query(User).filter_by(IDuser=data['userIDPublic']).first()
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Crear la publicación
        publicacion = Publicaciones(
            rutaImagen=data.get('rutaImagen'),
            contenido=data.get('contenido'),
            userIDPublic=data['userIDPublic']
        )
        db.add(publicacion)
        db.commit()

        return jsonify({
            "message": "Publicación creada exitosamente",
            "publicacion_id": publicacion.IDpublic
        }), 201






    @app.route('/list_publicaciones', methods=['GET'])
    def list_publicaciones():
        """
        Listar todas las publicaciones con detalles de usuario, total de likes, avatar del usuario y los primeros dos comentarios.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Cargar las relaciones necesarias
        publicaciones = db.query(Publicaciones).options(
            joinedload(Publicaciones.usuario),
            joinedload(Publicaciones.likes),
            joinedload(Publicaciones.comentarios).joinedload(Comments.usuario)
        ).all()

        # Estructura de salida
        publicacion_list = []
        for publicacion in publicaciones:
            # Obtener los primeros dos comentarios
            primeros_comentarios = publicacion.comentarios[:2]

            # Formatear los comentarios
            comentarios_list = [
                {
                    "IDcomments": comentario.IDcomments,
                    "contenido": comentario.contenido,
                    "fecha": comentario.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    "userIDComment": comentario.userIDComment,
                    "usuario": comentario.usuario.email,
                    "avatar": comentario.usuario.avatar
                }
                for comentario in primeros_comentarios
            ]

            publicacion_list.append({
                "IDpublic": publicacion.IDpublic,
                "rutaImagen": publicacion.rutaImagen,
                "contenido": publicacion.contenido,
                "fecha": publicacion.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "userIDPublic": publicacion.userIDPublic,
                "usuario": publicacion.usuario.email,
                "avatar": publicacion.usuario.avatar,
                "likes": len(publicacion.likes),  # Total de likes de la publicación
                "comentarios": comentarios_list
            })

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
    def create_like_route():
        """
        Crear un nuevo like asociado a una publicación, comentario o respuesta.
        """
        data = request.get_json()
        db = next(get_db())

        # Validar que exactamente uno de los IDs de destino esté presente
        destino_keys = ['publicIDLike', 'commentIDLike', 'answerIDLike']
        destino_present = [key for key in destino_keys if data.get(key)]
        if 'userIDLike' not in data or len(destino_present) != 1:
            return jsonify({"message": "Debe proporcionar 'userIDLike' y exactamente uno de 'publicIDLike', 'commentIDLike' o 'answerIDLike'"}), 400

        # Verificar la existencia del usuario
        usuario = db.query(User).filter_by(IDuser=data['userIDLike']).first()
        if not usuario:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Verificar si el objeto existe
        destino_key = destino_present[0]
        if destino_key == 'publicIDLike':
            objeto = db.query(Publicaciones).filter_by(IDpublic=data['publicIDLike']).first()
            if not objeto:
                return jsonify({"message": "Publicación no encontrada"}), 404
        elif destino_key == 'commentIDLike':
            objeto = db.query(Comments).filter_by(IDcomments=data['commentIDLike']).first()
            if not objeto:
                return jsonify({"message": "Comentario no encontrado"}), 404
        elif destino_key == 'answerIDLike':
            objeto = db.query(AnswersComments).filter_by(IDanswer=data['answerIDLike']).first()
            if not objeto:
                return jsonify({"message": "Respuesta no encontrada"}), 404

        # Verificar si el usuario ya dio like al objeto
        existing_like = db.query(Likes).filter(
            Likes.userIDLike == data['userIDLike'],
            Likes.publicIDLike == data.get('publicIDLike'),
            Likes.commentIDLike == data.get('commentIDLike'),
            Likes.answerIDLike == data.get('answerIDLike')
        ).first()
        if existing_like:
            return jsonify({"message": "El usuario ya ha dado like a este elemento"}), 400

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
        Listar likes con detalles de usuario, publicación, comentario y respuesta.
        Permite filtrar por 'publicIDLike', 'commentIDLike' o 'answerIDLike'.
        """
        db = next(get_db())
        public_id = request.args.get('publicIDLike', type=int)
        comment_id = request.args.get('commentIDLike', type=int)
        answer_id = request.args.get('answerIDLike', type=int)

        query = db.query(Likes)

        if public_id:
            query = query.filter(Likes.publicIDLike == public_id)
        if comment_id:
            query = query.filter(Likes.commentIDLike == comment_id)
        if answer_id:
            query = query.filter(Likes.answerIDLike == answer_id)

        likes = query.all()

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
#************************************
    @app.route('/comments/<int:public_id>', methods=['GET'])
    def list_comments_and_replies(public_id):
        """
        Lista todos los comentarios y sus respuestas para una publicación específica.
        Incluye los IDs de los comentarios y respuestas.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Verificar si la publicación existe
        publicacion = db.query(Publicaciones).filter_by(IDpublic=public_id).first()
        if not publicacion:
            return jsonify({"message": "Publicación no encontrada"}), 404

        # Cargar los comentarios y sus respuestas, junto con los usuarios y likes
        comentarios = db.query(Comments).options(
            joinedload(Comments.usuario),
            joinedload(Comments.likes),
            joinedload(Comments.respuestas).joinedload(AnswersComments.usuario),
            joinedload(Comments.respuestas).joinedload(AnswersComments.likes)
        ).filter_by(publicIDComment=public_id).all()

        # Ordenar los comentarios por fecha ascendente (opcional)
        comentarios.sort(key=lambda x: x.fecha)

        # Formatear los comentarios
        comentarios_list = []
        for comentario in comentarios:
            comentario_data = {
                "IDcomments": comentario.IDcomments,  # Agregado el ID del comentario
                "username": comentario.usuario.username,
                "avatar": comentario.usuario.avatar,
                "comment": comentario.contenido,
                "time": calculate_time_ago(comentario.fecha),
                "likes": len(comentario.likes),
                "replies": [],
                "isReplying": False
            }

            # Formatear las respuestas
            respuestas_ordenadas = sorted(comentario.respuestas, key=lambda x: x.fecha)
            for respuesta in respuestas_ordenadas:
                respuesta_data = {
                    "IDanswer": respuesta.IDanswer,  # Agregado el ID de la respuesta
                    "username": respuesta.usuario.username,
                    "avatar": respuesta.usuario.avatar,
                    "comment": respuesta.contenido,
                    "time": calculate_time_ago(respuesta.fecha),
                    "likes": len(respuesta.likes)
                }
                comentario_data["replies"].append(respuesta_data)

            comentarios_list.append(comentario_data)

        # Estructurar la respuesta con el ID de la publicación como clave
        response = {
            str(public_id): comentarios_list
        }

        return jsonify(response), 200
    def calculate_time_ago(fecha):
        """
        Calcula el tiempo transcurrido desde la fecha dada hasta ahora y lo devuelve en formato legible.
        """
        ahora = datetime.utcnow()
        diferencia = relativedelta(ahora, fecha)

        if diferencia.years > 0:
            return f"{diferencia.years} año{'s' if diferencia.years > 1 else ''}"
        elif diferencia.months > 0:
            return f"{diferencia.months} mes{'es' if diferencia.months > 1 else ''}"
        elif diferencia.days >= 7:
            semanas = diferencia.days // 7
            return f"{semanas} sem"
        elif diferencia.days > 0:
            return f"{diferencia.days} día{'s' if diferencia.days > 1 else ''}"
        elif diferencia.hours > 0:
            return f"{diferencia.hours} hora{'s' if diferencia.hours > 1 else ''}"
        elif diferencia.minutes > 0:
            return f"{diferencia.minutes} min"
        else:
            return "Justo ahora"

    @app.route('/posts_with_comments', methods=['GET'])
    def list_posts_with_comments():
        """
        Lista todas las publicaciones y, opcionalmente, filtra por usuario si se proporciona 'user_id'.
        Incluye comentarios y respuestas de comentarios.
        """
        db = next(get_db())  # Obtiene la sesión de base de datos

        # Obtener el 'user_id' de los parámetros de la URL (opcional)
        user_id = request.args.get('user_id', type=int)

        # Construir la consulta base
        query = db.query(Publicaciones).options(
            joinedload(Publicaciones.usuario),
            joinedload(Publicaciones.likes),
            joinedload(Publicaciones.comentarios).joinedload(Comments.usuario),
            joinedload(Publicaciones.comentarios).joinedload(Comments.likes),
            joinedload(Publicaciones.comentarios).joinedload(Comments.respuestas).joinedload(AnswersComments.usuario),
            joinedload(Publicaciones.comentarios).joinedload(Comments.respuestas).joinedload(AnswersComments.likes)
        )

        # Filtrar por 'user_id' si se proporciona
        if user_id:
            query = query.filter(Publicaciones.userIDPublic == user_id)

        publicaciones = query.all()

        # Formatear las publicaciones
        publicaciones_list = []
        for publicacion in publicaciones:
            publicacion_data = {
                "IDpublic": publicacion.IDpublic,
                "username": publicacion.usuario.username,
                "avatar": publicacion.usuario.avatar,
                "rutaImagen": publicacion.rutaImagen,
                "contenido": publicacion.contenido,
                "time": calculate_time_ago(publicacion.fecha),
                "likes": len(publicacion.likes),
                "comments": [],
            }

            # Ordenar los comentarios por fecha ascendente (opcional)
            comentarios_ordenados = sorted(publicacion.comentarios, key=lambda x: x.fecha)
            for comentario in comentarios_ordenados:
                comentario_data = {
                    "IDcomments": comentario.IDcomments,
                    "username": comentario.usuario.username,
                    "avatar": comentario.usuario.avatar,
                    "comment": comentario.contenido,
                    "time": calculate_time_ago(comentario.fecha),
                    "likes": len(comentario.likes),
                    "replies": [],
                    "isReplying": False
                }

                # Ordenar las respuestas por fecha ascendente (opcional)
                respuestas_ordenadas = sorted(comentario.respuestas, key=lambda x: x.fecha)
                for respuesta in respuestas_ordenadas:
                    respuesta_data = {
                        "IDanswer": respuesta.IDanswer,
                        "username": respuesta.usuario.username,
                        "avatar": respuesta.usuario.avatar,
                        "comment": respuesta.contenido,
                        "time": calculate_time_ago(respuesta.fecha),
                        "likes": len(respuesta.likes)
                    }
                    comentario_data["replies"].append(respuesta_data)

                publicacion_data["comments"].append(comentario_data)

            publicaciones_list.append(publicacion_data)

        return jsonify(publicaciones_list), 200