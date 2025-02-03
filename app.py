
from models.models import User, Room, Menssage # Importação de modelo de user para o app

from routes.auth import auth

from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, emit

from extensions import db, jwt
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY

from flask_sqlalchemy import SQLAlchemy

# Inicializa o Flask
app = Flask(__name__)
app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SECRET_KEY'] = SECRET_KEY

# Instância do SocketIO sem inicializar com app diretamente
socketio = SocketIO(cors_allowed_origins="*")

# Inicializa as extensões
# db.init_app(app) antiga inicialização
db = SQLAlchemy(app)

jwt.init_app(app)
socketio.init_app(app)


with app.app_context():
    db.create_all() # isso cria todas as tabelas defindas


@app.route('/')
def home():
    return {"message": "Bem-vindo ao SóPapo!"}

# Evento para quando um cliente entra na sala
@socketio.on('join_room')  
def handle_join_room(data):
    username = data.get('username')
    room = data.get('room')
    join_room(room)
    emit('receive_message', {'message': f'{username} entrou na sala {room}'}, room=room)

# Evento para quando um cliente sai da sala
@socketio.on('leave_room')  
def handle_leave_room(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit('receive_message', {'message': f'{username} saiu da sala {room}'}, room=room)

# Evento para envio de mensagens
@socketio.on('send_message')
def handle_send_message(data):
    username = data.get('username')
    room = data.get('room')
    message = data.get('message')
    emit('receive_message', {'message': f'{username}: {message}'}, room=room)

# Importação de rotas no final para evitar importação circular

app.register_blueprint(auth, url_prefix='/auth')

# Executa o servidor
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
