from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager

api = Api(
    title="Codemaze API",
    description="Interact with the Codemaze API through the routes below",
)
db = SQLAlchemy()
jwt = JWTManager()