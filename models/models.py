from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime
import uuid
from sqlalchemy import UUID, ForeignKey, String, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

def utcnow():
    return datetime.utcnow()

# ------------------ base model ------------------
class BaseModel(db.Model):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    created_at: Mapped[Optional[datetime]] = mapped_column(server_default=db.func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=db.func.now())

# ----------- user -> room association -----------
user_room_association = db.Table(
    'user_room',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True),
    db.Column('room_id', UUID(as_uuid=True), db.ForeignKey('rooms.id'), primary_key=True)
)

# ------------------- room db --------------------
class Room(BaseModel):
    __tablename__ = 'rooms'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    users: Mapped[list['User']] = relationship('User', secondary=user_room_association, back_populates='rooms')

# ------------------- user db --------------------
class User(BaseModel):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)  # Coluna email adicionada
    password_hash: Mapped[str] = mapped_column(nullable=False)
    rooms: Mapped[list['Room']] = relationship('Room', secondary=user_room_association, back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
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