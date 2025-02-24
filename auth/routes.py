from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity, create_access_token
from auth.jwt import create_token_pair
from models.models import User, BlackListToken
from extensions import db
from auth.hash import verify_password, get_password_hash
from auth.exception import BadRequestException, AuthorizationException
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