import socketio # type: ignore

# Cliente Socket.IO
sio = socketio.Client()

# Evento de conexão bem-sucedida
@sio.on('connect')
def on_connect():
    print("✅ Conectado ao servidor!")
    room = input("Digite o nome da sala: ")
    username = input("Digite o nome de usuário: ")
    sio.emit('join_room', {'username': username, 'room': room})
    while True:
        message = input("Digite uma mensagem: ")
        sio.emit('send_message', {'username': username, 'room': room, 'message': message})

# Evento para receber mensagens do servidor
@sio.on('receive_message')
def on_receive_message(data):
    print("📩 Mensagem recebida:", data['message'])

@sio.on('message')
def on_message(data):
    print(f"📩 {data['msg']}")

    
# Evento de desconexão
@sio.on('disconnect')
def on_disconnect():
    print("❌ Desconectado do servidor.")

# Conectar ao servidor
try:
    sio.connect('http://127.0.0.1:5000')
    print("🔗 Conexão estabelecida com o servidor!")

    # # Simular um usuário entrando em uma sala
    # sio.emit('join_room', {'username': 'TesteUser', 'room': 'Sala1'})

    # # Enviar mensagem de teste
    # sio.emit('send_message', {'username': 'TesteUser', 'room': 'Sala1', 'message': 'Olá, servidor!'})

    # Mantém o cliente ativo para receber respostas
    sio.wait()

except Exception as e:
    print("❌ Erro ao conectar:", str(e))
