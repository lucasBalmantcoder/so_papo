from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        """Gera e armazena o hash da senha"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

user_room_association = db.Table(
    'user_room',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_room_association, backref='rooms')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    # Indidicadores de envio de msg
    delivered = db.Column(db.Boolean, default=False) #se foi enviada
    read = db.Column(db.Boolean, default=False) #se foi lida



    

