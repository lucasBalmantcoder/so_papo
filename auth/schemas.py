import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime

# ----------------- JWT Token Schema -------------------

class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expires: datetime

class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema

# ----------------- User Schema -------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr

    # Configuração para suportar ORM
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID  # Use UUID em vez de str
    created_at: datetime

    # Configuração para suportar ORM
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str


class UserRegister(UserBase):
    password: str
    confirmed_password: str

    @field_validator("confirmed_password")
    def verificar_senha_match(cls, v, values):
        password = values.data["password"]  # ✅ Pydantic v2 usa `values.data[...]`

        if v != password:
            raise ValueError("As senhas devem ser iguais")
        return v

# ----------------- Token Blacklist Schema -------------------

class BlackListTokenSchema(BaseModel):
    id: str
    token: str
    created_at: datetime