import os

# Configuração básica
SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:mysenha@localhost:5432/sopapo')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secreto')
