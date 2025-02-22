from flask import Flask, jsonify
from extensions import db
from config import PG_URL

app = Flask(__name__)

# Configurar a URI do banco de dados corretamente
app.config["SQLALCHEMY_DATABASE_URI"] = PG_URL  
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Evita warnings

db.init_app(app)


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
