from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.models import User
from extensions import db

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    # Verifica se o usuário já existe
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Usuário já existe"}), 400

    # Registra um novo usuário
    new_user = User(username=username, password=password)

    # Cria e armazena a senha de forma segura
    new_user = User(username=username, email=email)
    new_user.set_password(password)  # Usa o método para hashear a senha

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    # Verifica credenciais
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"message": "Credenciais inválidas"}), 401

    # Cria um token de acesso
    token = create_access_token(identity=username)
    return jsonify({"token": token}), 200


