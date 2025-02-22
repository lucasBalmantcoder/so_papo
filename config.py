import os
from dotenv import load_dotenv
from pydantic import PostgresDsn

# Carrega variáveis do .env
load_dotenv()

# Nome da aplicação
APP_NAME = os.getenv("APP_NAME", "so_papo")

# Chave secreta
SECRET_KEY = os.getenv("SECRET_KEY")

# Configuração do banco de dados
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# URL do banco de dados
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuração do JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_EXPIRATION_DELTA = 3600  # Tempo de expiração do token (1 hora)

# Construindo a URL do PostgreSQL com Pydantic
PG_URL = PostgresDsn.build(
    scheme="postgresql",
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    path=f"/{POSTGRES_DB}",
)


