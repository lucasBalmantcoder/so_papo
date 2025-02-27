from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity, create_access_token
from auth.jwt import create_token_pair
from models.models import Message, Room, User, BlackListToken
from extensions import db
from auth.hash import verify_password, get_password_hash
from auth.exception import BadRequestException, AuthorizationException, NotFoundException
from auth.schemas import UserLogin, UserRegister, UserResponse

# 🔹 Criando um Blueprint
auth = Blueprint("auth", __name__)

GET = 'GET'
POST = 'POST'
DELETE = 'DELETE'
PUT = 'PUT'


@auth.route('/login', methods=[POST])
def login():
    """
    Rota de login. Retorna um par de tokens (access e refresh).
    """
    data = UserLogin(**request.json)
    user = User.query.filter_by(username=data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise BadRequestException('Invalid credentials (Username ou Senha inválidos)')

    user_schema = UserResponse.from_orm(user)
    token_pair = create_token_pair(user=user_schema)

    return jsonify({"access": token_pair.access.token, "refresh": token_pair.refresh.token}), 200

@auth.route('/register', methods=[POST])
def register():
    """
    Rota de registro. Cria um novo usuário.
    """
    data = UserRegister(**request.json)

    # Verifica se o e-mail já está cadastrado
    user = User.query.filter_by(email=data.email).first()
    if user:
        raise BadRequestException('Email already registered')

    # Cria o hash da senha
    password_hash = get_password_hash(data.password)

    # Cria o usuário com os dados corretos
    user = User(
        username=data.username,
        email=data.email,
        password_hash=password_hash,
    )
    user.is_active = True

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User successfully registered"}), 201

@auth.route('/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Rota para visualizar o perfil do usuário logado.
    Inclui a lista de salas em que o usuário é administrador.
    """
    print("Rota /user/profile acessada")  # Log para depuração

    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()
    print(f"ID do usuário logado: {logged_in_user_id}")  # Log para depuração

    # Busca o usuário no banco de dados
    user = User.query.filter_by(id=logged_in_user_id).first()
    if not user:
        print("Usuário não encontrado")  # Log para depuração
        raise NotFoundException('Usuário não encontrado')

    # Busca as salas em que o usuário é administrador (criador)
    admin_rooms = Room.query.filter_by(creator_id=user.id).all()
    admin_rooms_list = [
        {
            "room_id": str(room.id),
            "room_name": room.name,
            "created_at": room.created_at.isoformat() if room.created_at else None
        }
        for room in admin_rooms
    ]

    # Retorna as informações do usuário
    return jsonify({
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "admin_rooms": admin_rooms_list  # Lista de salas em que o usuário é administrador
    }), 200

@auth.route('/refresh', methods=[POST])
@jwt_required(refresh=True)  # Exige um refresh token
def refresh():
    """
    Rota de refresh. Gera um novo token de acesso a partir de um refresh token.
    """
    user_identity = get_jwt_identity()
    claims = get_jwt()

    # Verifica se o token é um refresh token
    if claims.get("type") != "refresh":
        raise AuthorizationException("Token inválido: não é um refresh token")

    # Cria um novo access token
    new_access_token = create_access_token(identity=user_identity)

    return jsonify({"access": new_access_token}), 200

@auth.route('/logout', methods=[POST])
@jwt_required()
def logout():
    """
    Rota de logout. Invalida o token atual.
    """
    jti = get_jwt()["jti"]

    if not jti:
        raise AuthorizationException("Invalid token")

    blacklisted_token = BlackListToken(token=jti)
    db.session.add(blacklisted_token)
    db.session.commit()

    return jsonify({"message": "Successfully logged out"}), 200

# ----------------- função de administrador -------------------

@auth.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()  # Obtém todos os usuários do banco de dados
    users_list = [
        {
            "id": str(user.id),  # Converte o UUID para string
            "username": user.username,
            "email": user.email
        }
        for user in users
    ]
    return jsonify(users_list), 200

@auth.route("/user/rooms", methods=["GET"])
@jwt_required()
def list_user_rooms():
    """
    Rota para listar todas as salas em que o usuário logado está participando.
    """
    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()

    # Busca o usuário logado
    user = User.query.filter_by(id=logged_in_user_id).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Formata a resposta com as salas do usuário
    rooms_list = []
    for room in user.rooms:
        rooms_list.append({
            "room_id": str(room.id),
            "room_name": room.name,
            "creator": room.creator.username,
            "created_at": room.created_at.isoformat() if room.created_at else None
        })

    return jsonify({"rooms": rooms_list}), 200

@auth.route("/create_room", methods=["POST"])
@jwt_required()
def create_room():
    print("Rota /create_room acessada")  # Verifica se a rota está sendo chamada

    data = request.get_json()
    print(f"Dados recebidos: {data}")  # Verifica os dados recebidos

    if not data or "name" not in data:
        print("Formato JSON inválido ou nome da sala ausente")
        return jsonify({"message": "Formato JSON inválido ou nome da sala ausente"}), 400

    room_name = data["name"]
    usernames = data.get("usernames", [])
    print(f"Nome da sala: {room_name}, Usuários: {usernames}")  # Verifica os dados processados

    # Obtém o ID do usuário logado a partir do token JWT
    logged_in_user_id = get_jwt_identity()
    print(f"ID do usuário logado (from JWT): {logged_in_user_id}")  # Verifica o ID do usuário logado

    # Busca o usuário pelo ID (UUID)
    creator = User.query.filter_by(id=logged_in_user_id).first()
    if not creator:
        print(f"Usuário não encontrado: {logged_in_user_id}")
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Verifica se já existe uma sala com o mesmo nome
    if Room.query.filter_by(name=room_name).first():
        print(f"Sala já existe: {room_name}")
        return jsonify({"message": "Já existe uma sala com esse nome"}), 400

    # Cria a nova sala e define o criador
    new_room = Room(name=room_name, creator_id=creator.id)
    new_room.users.append(creator)  # Adiciona o criador à sala

    # Adiciona os outros usuários encontrados
    not_found_users = []
    for username in usernames:
        if username == creator.username:  # Ignora o criador, pois ele já foi adicionado
            continue
        user = User.query.filter_by(username=username).first()
        if user:
            new_room.users.append(user)
        else:
            not_found_users.append(username)
    print(f"Usuários não encontrados: {not_found_users}")  # Verifica usuários não encontrados

    try:
        db.session.add(new_room)
        db.session.commit()
        print(f"Sala salva no banco de dados com ID: {new_room.id}")  # Verifica se a sala foi salva
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
        db.session.rollback()
        return jsonify({"message": "Erro ao salvar no banco de dados"}), 500

    response = {
        "message": "Sala criada com sucesso",
        "room_id": str(new_room.id),
        "room_name": new_room.name,
        "creator": creator.username,
        "users": [user.username for user in new_room.users],
    }

    if not_found_users:
        response["not_found_users"] = not_found_users

    return jsonify(response), 201



@auth.route("/rooms", methods=["GET"])
@jwt_required()
def list_rooms():
    """
    Rota para listar todas as salas criadas.
    """
    # Busca todas as salas no banco de dados
    rooms = Room.query.all()

    # Formata a resposta
    rooms_list = []
    for room in rooms:
        rooms_list.append({
            "room_id": str(room.id),
            "room_name": room.name,
            "creator": room.creator.username,  # Nome do criador da sala
            "created_at": room.created_at.isoformat() if room.created_at else None,
            "updated_at": room.updated_at.isoformat() if room.updated_at else None
        })

    return jsonify({"rooms": rooms_list}), 200


@auth.route("/rooms/<uuid:room_id>", methods=[GET])
@jwt_required()
def list_room_users(room_id):
    """
    Rota para listar todos os usuários de uma sala específica.
    """
    print(f"Buscando usuários da sala: {room_id}")  # Log para depuração

    # Busca a sala pelo ID
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        print(f"Sala não encontrada: {room_id}")  # Log para depuração
        return jsonify({"message": "Sala não encontrada"}), 404

    # Formata a resposta com os usuários da sala
    users_list = []
    for user in room.users:
        print(f"Usuário encontrado: {user.username}")  # Log para depuração
        users_list.append({
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email
        })

    return jsonify({
        "room_id": str(room.id),
        "room_name": room.name,
        "users": users_list
    }), 200


@auth.route("/rooms/<uuid:room_id>", methods=["DELETE"])
@jwt_required()
def delete_room(room_id):
    """
    Rota para apagar uma sala específica.
    Apenas o criador da sala pode apagá-la.
    """
    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()

    # Busca a sala pelo ID
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return jsonify({"message": "Sala não encontrada"}), 404

    # Verifica se o usuário logado é o criador da sala
    if str(room.creator_id) != logged_in_user_id:
        return jsonify({"message": "Apenas o criador da sala pode apagá-la"}), 403

    # Remove a sala do banco de dados
    db.session.delete(room)
    db.session.commit()

    return jsonify({"message": "Sala apagada com sucesso"}), 200


# ----------------- para um usuário logado entrar em uma sala -------------------
@auth.route("/rooms/<uuid:room_id>/join", methods=[POST])
@jwt_required()
def join_room(room_id):
    """
    Rota para um usuário logado entrar em uma sala.
    """
    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()

    # Busca o usuário logado
    user = User.query.filter_by(id=logged_in_user_id).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Busca a sala pelo ID
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return jsonify({"message": "Sala não encontrada"}), 404

    # Verifica se o usuário já está na sala
    if user in room.users:
        return jsonify({"message": "Usuário já está na sala"}), 400

    # Adiciona o usuário à sala
    room.users.append(user)
    db.session.commit()

    return jsonify({"message": "Usuário entrou na sala com sucesso"}), 200


# ----------------- para um usuário logado se remover de uma sala -------------------
@auth.route("/rooms/<uuid:room_id>/leave", methods=["POST"])
@jwt_required()
def leave_room(room_id):
    """
    Rota para um usuário logado se remover de uma sala.
    """
    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()

    # Busca o usuário logado
    user = User.query.filter_by(id=logged_in_user_id).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Busca a sala pelo ID
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return jsonify({"message": "Sala não encontrada"}), 404

    # Verifica se o usuário está na sala
    if user not in room.users:
        return jsonify({"message": "Usuário não está na sala"}), 400

    # Remove o usuário da sala
    room.users.remove(user)
    db.session.commit()

    return jsonify({"message": "Usuário saiu da sala com sucesso"}), 200

# ----------------- para o admin da sala remover um usuário -------------------
@auth.route("/rooms/<uuid:room_id>/remove_user/<uuid:user_id>", methods=["DELETE"])
@jwt_required()
def remove_user_from_room(room_id, user_id):
    """
    Rota para o administrador da sala remover um usuário.
    """
    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()

    # Busca a sala pelo ID
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return jsonify({"message": "Sala não encontrada"}), 404

    # Verifica se o usuário logado é o criador da sala
    if str(room.creator_id) != logged_in_user_id:
        return jsonify({"message": "Apenas o criador da sala pode remover usuários"}), 403

    # Busca o usuário a ser removido
    user_to_remove = User.query.filter_by(id=user_id).first()
    if not user_to_remove:
        return jsonify({"message": "Usuário a ser removido não encontrado"}), 404

    # Verifica se o usuário está na sala
    if user_to_remove not in room.users:
        return jsonify({"message": "Usuário não está na sala"}), 400

    # Remove o usuário da sala
    room.users.remove(user_to_remove)
    db.session.commit()

    return jsonify({"message": "Usuário removido da sala com sucesso"}), 200

@auth.route("/rooms/<uuid:room_id>/add_user/<uuid:user_id>", methods=["POST"])
@jwt_required()
def add_user_to_room(room_id, user_id):
    """
    Rota para o criador da sala adicionar um usuário à sala.
    """
    # Obtém o ID do usuário logado
    logged_in_user_id = get_jwt_identity()

    # Busca a sala pelo ID
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return jsonify({"message": "Sala não encontrada"}), 404

    # Verifica se o usuário logado é o criador da sala
    if str(room.creator_id) != logged_in_user_id:
        return jsonify({"message": "Apenas o criador da sala pode adicionar usuários"}), 403

    # Busca o usuário a ser adicionado
    user_to_add = User.query.filter_by(id=user_id).first()
    if not user_to_add:
        return jsonify({"message": "Usuário a ser adicionado não encontrado"}), 404

    # Verifica se o usuário já está na sala
    if user_to_add in room.users:
        return jsonify({"message": "Usuário já está na sala"}), 400

    # Adiciona o usuário à sala
    room.users.append(user_to_add)
    db.session.commit()

    return jsonify({"message": "Usuário adicionado à sala com sucesso"}), 200


# ----------------- implementação de chat -------------------

@auth.route('/messages', methods=[POST])
@jwt_required()
def send_message():
    data = request.json
    room_id = data.get('room_id')
    message = data.get('message')

    if not room_id or not message:
        raise BadRequestException('Room ID and message are required')

    room = Room.query.filter_by(id=room_id).first()
    if not room:
        raise BadRequestException('Sala não encontrada')

    user_id = get_jwt_identity()

    new_message = Message(
        room_id=room_id,
        message=message,
        user_id=user_id  # Apenas o user_id é necessário
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully"}), 201



@auth.route('/messages/<room_id>', methods=['GET'])
@jwt_required()
def get_messages(room_id):
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        raise NotFoundException('Room not found')

    messages = Message.query.filter_by(room_id=room.id).all()

    messages_list = [
        {
            "user_id": message.user_id,
            "username": message.user.username,  # Obtido via relacionamento
            "message": message.message,
            "timestamp": message.timestamp.isoformat() if message.timestamp else None,
            "delivered": message.delivered,
            "read": message.read
        }
        for message in messages
    ]

    return jsonify({"messages": messages_list}), 200







@auth.route('/messages/<message_id>/delivered', methods=[PUT])
@jwt_required()
def mark_message_delivered(message_id):
    """
    Rota para marcar uma mensagem como entregue.
    """
    # Busca a mensagem no banco
    message = Message.query.filter_by(id=message_id).first()
    if not message:
        raise NotFoundException('Message not found')

    # Marca a mensagem como entregue
    message.delivered = True
    db.session.commit()

    return jsonify({"message": "Message marked as delivered"}), 200


@auth.route('/messages/<message_id>/read', methods=[PUT])
@jwt_required()
def mark_message_read(message_id):
    """
    Rota para marcar uma mensagem como lida.
    """
    # Busca a mensagem no banco
    message = Message.query.filter_by(id=message_id).first()
    if not message:
        raise NotFoundException('Message not found')

    # Marca a mensagem como lida
    message.read = True
    db.session.commit()

    return jsonify({"message": "Message marked as read"}), 200



# ----------------- rota para editar o nome de uma room -------------------

# @auth.route("/create_room", methods=["POST"])
# @jwt_required()
# def create_room():
#     """
#     Rota para criar uma nova sala.
#     O usuário logado será automaticamente adicionado à sala como criador.
#     Outros usuários podem ser adicionados opcionalmente.
#     """
#     data = request.get_json()

#     # Valida o JSON recebido
#     if not data or "name" not in data:
#         return jsonify({"message": "Formato JSON inválido ou nome da sala ausente"}), 400

#     room_name = data["name"]
#     usernames = data.get("usernames", [])  # Lista opcional de usuários

#     # Obtém o username do usuário logado
#     # logged_in_username = get_jwt_identity()

#     # Verifica se o usuário logado existe no banco de dados
#     # logged_in_username = get_jwt_identity()
#     # print(f"Usuário logado (from JWT): {logged_in_username}")
#     # creator = User.query.filter_by(username=logged_in_username).first()
#     # if not creator:
#     #     return jsonify({"message": "Usuário não encontrado"}), 404

#     # Verifica se já existe uma sala com o mesmo nome
#     if Room.query.filter_by(name=room_name).first():
#         return jsonify({"message": "Já existe uma sala com esse nome"}), 400

#     # Cria a nova sala e define o criador
#     # new_room = Room(name=room_name, creator_id=creator.id)
#     new_room = Room(name=room_name)
#     # new_room.users.append(creator)  # Adiciona o criador à sala

#     # Adiciona os outros usuários encontrados
#     not_found_users = []
#     for username in usernames:
#         user = User.query.filter_by(username=username).first()
#         if user:
#             new_room.users.append(user)
#         else:
#             not_found_users.append(username)

#     # Salva no banco de dados
#     db.session.commit()

#     response = {
#         "message": "Sala criada com sucesso",
#         "room_id": str(new_room.id),
#         "room_name": new_room.name,
#         # "creator": creator.username,
#         "users": [user.username for user in new_room.users],
#     }

#     if not_found_users:
#         response["not_found_users"] = not_found_users

#     return jsonify(response), 201

