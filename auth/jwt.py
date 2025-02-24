from datetime import datetime, timedelta
import uuid
from jose import JWTError
import jwt
from auth.exception import AuthorizationException
from auth.schemas import JwtTokenSchema, TokenPair
from config import REFRESH_TOKEN_EXPIRES_MINUTES, SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models.models import BlackListToken, User


def _create_token(payload: dict, minutes: int | None = None, is_refresh: bool = False) -> JwtTokenSchema:
    """
    Cria um token JWT com um payload personalizado.
    :param payload: Dados a serem incluídos no token.
    :param minutes: Tempo de expiração em minutos.
    :param is_refresh: Define se é um refresh token.
    :return: Objeto JwtTokenSchema contendo o token e seus detalhes.
    """
    expire = datetime.utcnow() + timedelta(minutes=minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    payload['exp'] = expire
    payload["type"] = "refresh" if is_refresh else "access"  # Define o tipo de token

    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    print(f"Token gerado ({'refresh' if is_refresh else 'access'}):", jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM]))
    
    return JwtTokenSchema(
        token=token,
        payload=payload,
        expires=expire
    )


def create_token_pair(user: User) -> TokenPair:
    """
    Cria um par de tokens (access e refresh) para um usuário.
    :param user: Objeto do usuário.
    :return: Objeto TokenPair contendo os tokens.
    """
    payload = {"sub": str(user.id), "name": user.username, "jti": str(uuid.uuid4())}
    return TokenPair(
        access=_create_token(payload, minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        refresh=_create_token(payload, minutes=REFRESH_TOKEN_EXPIRES_MINUTES, is_refresh=True),
    )


def decode_access_token(token: str): # n usado atualmente
    """
    Decodifica um token de acesso e verifica se ele é válido.
    :param token: Token JWT.
    :return: Payload do token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("frs"):
            raise JWTError("Access token needed")
        if BlackListToken.query.filter_by(id=payload["jti"]).first():
            raise JWTError("Token is blacklisted")
    except JWTError:
        raise AuthorizationException()
    return payload