# from flask import Blueprint, request, jsonify
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from auth.jwt import create_token_pair
from models.models import User
from extensions import db
from hash import get_password_hash, verify_password
from exception import *
from app import app


from auth.schemas import (
    UserLogin,
    User as UserSchema
)

GET = 'GET'
POST = 'POST'
DELETE = 'DELETE'
PUT = 'PUT'

@app.route('/login', methods=[POST])
def login():
    data = UserLogin(**request.json)
    user = User.query.filter_by(email=data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise BadRequestException('Invalid credentials (Email ou Senha inválidos)')
    
    token_pair = create_token_pair(user=UserSchema.from_orm(user))

    return {"access": token_pair.access.token, "refresh": token_pair.refresh.token}, 

@app.route('/register', methods=[POST])
def register():
    data = UserLogin(**request.json)
    user = User.query.filter_by(email=data.email).first()

    if user:
        raise BadRequestException('Email already registered')
    
    # colocando hash 
    user_data = data.dict(exclude={'confirm_password'})
    user_data['password'] = get_password_hash(user_data['password'])

    #salvando no db
    user = User(**user_data)
    user.is_active = True
    