from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from auth.routes import auth
from extensions import db
# from auth import auth
from config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    JWT_SECRET_KEY,
    JWT_TOKEN_LOCATION,
    JWT_ACCESS_TOKEN_EXPIRES,
    JWT_REFRESH_TOKEN_EXPIRES,
)

# Inicializa o Flask
app = Flask(__name__)

# Configurações do Flask
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configurações do Flask-JWT-Extended
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = JWT_TOKEN_LOCATION
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = JWT_REFRESH_TOKEN_EXPIRES

# Inicializa as extensões
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  # Inicializa o Flask-Migrate

# Registra o blueprint de autenticação
app.register_blueprint(auth, url_prefix='/auth')   # Rota de autenticação (login, registro)

if __name__ == '__main__':
    with app.app_context():
        # Testa a conexão com o banco de dados
        try:
            db.engine.connect()
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

        # Cria as tabelas (se não existirem)
        db.create_all()

        # Adiciona um usuário de teste (opcional)
        try:
            # user = User(username='testuser', email='test@example.com')
            # user.set_password('senha_segura')
            # db.session.add(user)
            # db.session.commit()
            print("Usuário de teste adicionado!")
        except Exception as e:
            print(f"Erro ao adicionar usuário de teste: {e}")






# ----------------- Antigo projeto -------------------

# from flask import Flask, render_template, request 
# from flask_jwt_extended import JWTManager
# from flask_socketio import join_room, leave_room, emit 
# # from flask_sqlalchemy import SQLAlchemy
# from extensions import db, jwt, socketio # isso importa as extensões
# from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
# from models.models import User, Room, Message 
# from routes.auth import auth  # Importação de rotas
# from sockets import socketio
# from flask_cors import CORS

# __name__= "__sopapo__"

# # Inicializa o Flask
# app = Flask(__name__)
# app.config.from_object('config')
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
# jwt = JWTManager(app)

# # Inicializa as extensões
# db.init_app(app)
# jwt.init_app(app)
# socketio.init_app(app)

# with app.app_context():
#     print("Criando tabelas no banco de dados...")
#     db.create_all()

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return "A api está rodando!"



# # Importação de rotas no final para evitar importação circular
# app.register_blueprint(auth)

# # Executa o servidor
# if __name__ == '__main__':
#     # socketio.run(app, debug=True)
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)
