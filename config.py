import os
from dotenv import load_dotenv
from datetime import timedelta

# Carrega variáveis do .env
load_dotenv()

# Nome da aplicação
APP_NAME = os.getenv("APP_NAME", "so_papo")

# Configurações do banco de dados
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:mysenha@localhost/pjdb")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Chave secreta da aplicação (deve ser segura e única para cada projeto)
SECRET_KEY = os.getenv("SECRET_KEY", "uma_chave_secreta_segura")

# Configurações do Flask-JWT-Extended
JWT_SECRET_KEY = SECRET_KEY  # Garante que a mesma chave seja usada para assinar e validar tokens
JWT_TOKEN_LOCATION = ["headers"]  # O token será enviado no cabeçalho da requisição
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  # O token de acesso expira em 30 minutos
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)  # O token de refresh expira em 1 dia
JWT_ALGORITHM = "HS256"  # Algoritmo de assinatura do JWT

# Configurações de compatibilidade (mantendo as variáveis antigas)
REFRESH_TOKEN_EXPIRES_MINUTES = 1440  # 24 horas
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
ALGORITMO = JWT_ALGORITHM  # Mantém o mesmo algoritmo configurado

# Outras configurações
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")




# # Configuração do banco de dados
# POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysenha")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# POSTGRES_DB = os.getenv("POSTGRES_DB", "pjdb")

# # URL do banco de dados
# SQLALCHEMY_DATABASE_URI = os.getenv(
#     "DATABASE_URL",
#     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )
# SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuração do JWT
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "outra_chave_secreta_muito_segura")
# JWT_EXPIRATION_DELTA = 3600  # Tempo de expiração do token (1 hora)