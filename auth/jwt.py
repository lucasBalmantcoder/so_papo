from datetime import datetime, timedelta
import uuid
from jose import JWTError
import jwt
from auth.exception import AuthorizationException
from auth.schemas import JwtTokenSchema, TokenPair
from config import REFRESH_TOKEN_EXPIRES_MINUTES,SECRET_KEY, ALGORITMO, ACCESS_TOKEN_EXPIRE_MINUTES
from models.models import BlackListToken, User


def _create_token(payload: dict, minutes: int| None = None) -> JwtTokenSchema:
    expire = datetime.utcnow() + timedelta(
        minutes=minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload['exp'] = expire
    payload["frs"] = False

    return JwtTokenSchema(
        token=jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO),
        payload=payload,
        expires=expire
    )



# jti - é p indetificador único para o token
# é gerado pelo uuid.uuid4()

def create_token_pair(user: User) -> TokenPair:
    payload = {"sub": str(user.id), "name": user.username, "jti": str(uuid.uuid4())}
    return TokenPair(
        access=_create_token(payload, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)),
        refresh=_create_token(payload, timedelta(minutes=REFRESH_TOKEN_EXPIRES_MINUTES), is_refresh=True),
    )

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        if payload.get("frs"):
            raise JWTError("Access token needed")
        if BlackListToken.query.filter_by(id=payload["jti"]).first():
            raise JWTError("Token is blacklisted")
    except JWTError:
        raise AuthorizationException()
    return payload


def refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        if not payload.get("frs"):
            raise JWTError("Refresh token needed")
    except JWTError:
        raise AuthorizationException()
    return {"access": _create_token(payload, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).token}