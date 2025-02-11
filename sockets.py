from urllib import request
from flask_socketio import join_room, leave_room, emit
from extensions import db, socketio
from models.models import Room, Message

# Evento para quando um cliente entra na sala
@socketio.on('join_room')
def handle_join_room(data):
    """Gerência user para entrar na sala"""
    username = data.get('username')
    room_name = data.get('room')

    # verificar se a sala existe no db
    room = Room.query.filter_by(name=room_name).first()


    if room:
        join_room(room_name)
        emit('receive_message', {'message': f'{username} entrou na sala {room_name}'}, room=room)
    else:
        emit('erro', {'message': f' sala {room_name} não encontrada '}, room=request.sid)

# Evento para quando um cliente sai da sala
@socketio.on('leave_room')  
def exit_room(data):
    username = data.get('username')
    room = data.get('room')
    leave_room(room)
    emit('receive_message', {'message': f'{username} saiu da sala {room}'}, room=room)


# Evento para envio de mensagens
@socketio.on('send_message')
def handle_send_message(data):
    username = data.get('username')
    room_name = data.get('room')
    message_content = data.get('message')

    if not username or not room_name or not message_content:
        emit('error', {'message': 'Dados inválidos para enviar a mensagem'}, room=request.sid)
        return

    # Criar e salvar a mensagem no banco de dados
    new_message = Message(username=username, room=room_name, content=message_content)
    db.session.add(new_message)
    db.session.commit()

    # Emitir a mensagem com o ID salvo no banco para controle
    emit('receive_message', {
        'message_id': new_message.id,
        'username': username,
        'message': message_content,
        'timestamp': new_message.timestamp.isoformat(),
        'delivered': new_message.delivered,
        'read': new_message.read
    }, room=room_name)


@socketio.on('message_delivered')
def mensage_delivered(data):
    message_id = data.get('message_id')
    message = Message.query.get(message_id)
    if message:
        message.delivered = True
        db.session.commit()
        emit('receive_message', {'message_id': message_id, 'delivered': True}, broadcast=True)

@socketio.on('message_read')
def mensage_read(data):
    message_id = data.get('message_id')
    message = Message.query.get(message_id)
    if message:
        message.read = True
        db.session.commit()
        emit('receive_message', {'message_id': message_id, 'read': True}, broadcast=True)
