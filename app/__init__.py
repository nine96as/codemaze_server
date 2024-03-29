import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import api, db, jwt, socketio, cors
from .seed import initialize_db
from .routers.auth import authRouter
from .routers.users import userRouter
from .routers.problems import problemRouter
from .routers.sessions import sessionRouter
from .routers.sockets import sockets
from .models import TokenBlocklist, User

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("PROD_DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["SECRET_KEY"] = "secret"

    allowed_origins = [
        "https://codemaze.onrender.com/",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ]

    cors.init_app(app, origins=allowed_origins)
    api.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins=allowed_origins)

    api.add_namespace(authRouter)
    app.register_blueprint(sockets)
    api.add_namespace(userRouter)
    api.add_namespace(problemRouter)
    api.add_namespace(sessionRouter)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).first()

    # Seed test data (no longer required)
    # initialize_db(app, db)

    return app
