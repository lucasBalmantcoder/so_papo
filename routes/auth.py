from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.models import User, Room, Message
from extensions import db

from flask_jwt_extended import jwt_required, get_jwt_identity

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    #verificar depois como arrumar
    return jsonify({"message": "Logout realizado com sucesso"}), 200


@auth.route('/profile', methods=['GET']) # type: ignore
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Bem-vindo, {current_user}"})

# Registra o Blueprint SEM um prefixo
auth = Blueprint('auth', __name__)

# auth = Blueprint('auth', __name__)

#mostra todos os users salvos no db
@auth.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(users_list), 200

#faz o registro de user no bd
@auth.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Formato JSON inválido ou ausente"}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return jsonify({"message": "Todos os campos são obrigatórios"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Usuário já existe"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Armazena a senha com hash

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso"}), 201

# Rota para apagar o usuário do banco de dados com base no nome e email
@auth.route("/delete_user", methods=['DELETE'])
def delete_user():
    data = request.get_json()  # Obtém os dados da requisição

    # Verifica se o nome de usuário e email foram fornecidos
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"message": "Nome de usuário e email são obrigatórios"}), 400

    # Busca o usuário com o nome de usuário e email fornecidos
    user = User.query.filter_by(username=username, email=email).first()
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Deleta o usuário encontrado
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Usuário deletado com sucesso"}), 200

#faz o login
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Formato JSON inválido ou ausente"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Usuário e senha são obrigatórios"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Credenciais inválidas"}), 401

    token = create_access_token(identity=username)
    return jsonify({"token": token}), 200
    # print(token)


#rotas para salas

@auth.route("/create_room", methods=['POST'])
def create_room():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Formato JSON inválido ou ausente"}), 400

    room_name = data.get('name')

    if not room_name:
        return jsonify({"message": "O nome da sala é obrigatório"}), 400

    # Verifica se já existe uma sala com esse nome
    if Room.query.filter_by(name=room_name).first():
        return jsonify({"message": "Já existe uma sala com esse nome"}), 400

    new_room = Room(name=room_name)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({"message": "Sala criada com sucesso", "room_id": new_room.id}), 201


@auth.route("/rooms", methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    rooms_list = [{"id": room.id, "name": room.name} for room in rooms]
    return jsonify(rooms_list), 200



#rotas para mensagens
@auth.route("/send_message", methods=['POST'])
def send_message():
    '''Função que faz envio de mensagens, para o user que está na sala atual'''
    '''e aṕos, salva no db e retorna a mensagem com o id salvo no db'''
    data = request.get_json()
    
    username = data.get("username")
    room_id = data.get("room_id")
    message_content = data.get("message")
    user_id = data.get("user_id")

    if not username or not room_id or not message_content or not user_id:
        return jsonify({"message": "Dados inválidos para enviar a mensagem"}), 400

    room = Room.query.get(room_id)  # .get() recebe apenas o ID diretamente
    user = User.query.get(user_id)

    if not room or not user:
        return jsonify({    "message": "Sala ou usuário não encontrados" }), 404
    
    # Criar e salvar a mensagem no banco de dados
    new_message = Message(
        username=username,
        room_id=room_id,
        user_id=user_id,
        message = message_content,
        timestamp=datetime.now()
        )
    db.session.add(new_message)
    db.session.commit()


    #saída da api para o frontend
    return jsonify({
        "message_id": new_message.id,
        "username": username,
        "message" : message_content,
        "timestamp": new_message.timestamp.isoformat()

    }), 201

    # Emitir a mensagem com o ID salvo no banco para controle

@auth.route("/join_room", methods=['POST'])
def join_room():
    """Adiciona um usuário a uma sala existente."""
    data = request.get_json()

    user_id = data.get("user_id")
    room_id = data.get("room_id")


    # Verifica se os IDs são números inteiros
    try:
        user_id = int(user_id)
        room_id = int(room_id)
    except ValueError:
        return jsonify({"message": "IDs de usuário e sala devem ser números inteiros"}), 400

    # Verifica se a sala e o usuário existem
    room = Room.query.get(room_id)
    user = User.query.get(user_id)

    if not room:
        return jsonify({"message": "Sala não encontrada"}), 404
    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    # Adiciona o usuário à sala (Aqui depende da sua modelagem, veja abaixo)
    if hasattr(room, 'users') and user not in room.users:
        room.users.append(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user.username} entrou na sala {room.name}"}), 200
    else:
        return jsonify({"message": "Usuário já está na sala ou não há suporte para essa funcionalidade"}), 400
