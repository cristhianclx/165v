import datetime
from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = "2025.happy.new.year"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)

ma = Marshmallow(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    language = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id)


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "age",
            "country",
            "city",
            "address",
            "created_at"
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


user_schema = UserSchema()
users_schema = UserSchema(many = True)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")
    
    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.Schema):
    user = ma.Nested(UserSchema)
    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "content",
            "created_at",
            "user",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


class MessageBasicSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "content",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_basic_schema = MessageBasicSchema()
messages_basic_schema = MessageBasicSchema(many = True)


@app.route("/login", methods=["POST"])
def login():
    id = request.json.get("id", None)
    password = request.json.get("password", None)
    if id != "cristhian" or password != "123456":
        return {"msg": "Bad username or password"}, 401
    access_token = create_access_token(identity=id)
    return {"access_token": access_token}


@app.route("/public/")
def public():
    return {
        "env": "public"
    }


@app.route("/private/")
@jwt_required()
def private():
    current_user = get_jwt_identity()
    return {
        "env": "private",
        "user": current_user,
    }


@app.route("/messages/")
@jwt_required()
def messages():
    current_user = get_jwt_identity()
    user = User.query.filter_by(name = current_user).first()
    if user:
        items = Message.query.filter_by(user = user)
        return messages_basic_schema.dump(items)
    else:
        return []