import os
from dotenv import load_dotenv

load_dotenv()

# Configuração básica da aplicaçaão
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_EXPIRATION_DELTA = 3600  # Tempo de expiração do token (1 hora)