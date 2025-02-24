from flask import Flask
from flask_jwt_extended import JWTManager
from config import *
from extensions import db
from models.models import User



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = PG_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

db.init_app(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    with app.app_context():
        # test_user = User(username="testuser", email="test@example.com", password_hash="dummyhash")
        # db.session.add(test_user)
        # db.session.commit()
    # print("Usuário de teste adicionado!")
app.run(debug=True)
