import os

# Configuração básica
SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///sopapo.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secreto')
