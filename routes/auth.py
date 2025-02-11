from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.models import User, Room
from extensions import db

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
    print(token)


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


# @auth.route("/join_room", methods=['POST'])