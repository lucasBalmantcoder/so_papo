from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime
import uuid
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

def utcnow():
    return datetime.utcnow()

# ------------------ base model ------------------
class BaseModel(db.Model):
    __abstract__ = True
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=utcnow())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=utcnow())

# --------------- user base model ----------------
class User(BaseModel):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(unique=True, nullable=False, length=100)
    password_hash: Mapped[str] = mapped_column(nullable=False, length=256)
    email: Mapped[str] = mapped_column(nullable=False, length=120)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()

# ----------- user -> room association -----------
user_room_association = db.Table(
    'user_room',
    db.Column('user_id', db.String, db.ForeignKey('users.id')),
    db.Column('room_id', db.String, db.ForeignKey('rooms.id'))
)

# ------------------- room db --------------------
class Room(BaseModel):
    __tablename__ = 'rooms'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    users: Mapped[list[User]] = relationship('User', secondary=user_room_association, backref='rooms')

# ---------------- class message -----------------
class Message(BaseModel):
    __tablename__ = 'messages'
    username: Mapped[str] = mapped_column(nullable=False)
    room_id: Mapped[str] = mapped_column(ForeignKey('rooms.id'))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    timestamp: Mapped[datetime] = mapped_column(default=utcnow())
    delivered: Mapped[bool] = mapped_column(default=False)
    read: Mapped[bool] = mapped_column(default=False)

# ---------------- Blacklist Token --------------
class BlackListToken(BaseModel):
    __tablename__ = 'blacklist_tokens'
    token: Mapped[str] = mapped_column(unique=True, nullable=False)



# class User(db.Model):
#     __tablename__ = 'users'
#     id: Mapped[uuid.UUID] = mapped_column(
#         primary_key=True, index=True, default=uuid.uuid4
#     )
#     username: Mapped[str] = mapped_column(unique=True, nullable=False, length=100)
#     password_hash: Mapped[str] = mapped_column(nullable=False, length=256)
#     email: Mapped[str] = mapped_column(nullable=False, length=80, length=120)

#     def set_password(self, password):
#         """Gera e armazena o hash da senha"""
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         """Verifica se a senha fornecida corresponde ao hash armazenado"""
#         return check_password_hash(self.password_hash, password)

#     @staticmethod
#     def find_by_username(username):
#         """Procura um usuário pelo nome de usuário"""
#         return User.query.filter_by(username=username).first()

#     def __repr__(self):
#         return f'<User {self.username}>'

# # Associação entre usuários e salas
# user_room_association = db.Table(
#     'user_room',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'))
# )

# class Room(db.Model):
#     __tablename__ = 'rooms'
#     id: Mapped[uuid.UUID] = mapped_column(
#         primary_key=True, index=True, default=uuid.uuid4
#     )
#     name: Mapped[str] = mapped_column(unique=True, nullable=False)
#     users: Mapped[list[User]] = relationship('User', secondary=user_room_association, backref='rooms')

# class Message(db.Model):
#     __tablename__ = 'messages'
#     id: Mapped[uuid.UUID] = mapped_column(
#         primary_key=True, index=True, default=uuid.uuid4
#     )
#     username: Mapped[str] = mapped_column(nullable=False)
#     room_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rooms.id'))
#     message: Mapped[str] = mapped_column(Text, nullable=False)
#     user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'))
#     timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
#     delivered: Mapped[bool] = mapped_column(default=False)  # Se foi enviada
#     read: Mapped[bool] = mapped_column(default=False)  # Se foi lida
