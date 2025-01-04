from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

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


class IndexResource(Resource):
    def get(self):
        return {
            "status": "working"
        }


class UsersResource(Resource):
    def get(self):
        items = User.query.all()
        return users_schema.dump(items)

    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item), 201


class UsersIDResource(Resource):
    def get(self, id):
        item = User.query.get_or_404(id)
        return user_schema.dump(item)
    
    def patch(self, id):
        item = User.query.get_or_404(id)
        data = request.get_json()
        item.name = data.get("name", item.name)
        item.age = data.get("age", item.age)
        item.country = data.get("country", item.country)
        item.city = data.get("city", item.city)
        item.address = data.get("address", item.address)
        item.language = data.get("language", item.language)
        db.session.add(item)
        db.session.commit()
        return user_schema.dump(item)

    def delete(self, id):
        item = User.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class MessagesResource(Resource):
    def get(self):
        items = Message.query.all()
        return messages_schema.dump(items)
    
    def post(self):
        data = request.get_json()
        item = Message(**data)
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item), 201


class MessagesIDResource(Resource):
    def get(self, id):
        item = Message.query.get_or_404(id)
        return message_schema.dump(item)
    
    def patch(self, id):
        item = Message.query.get_or_404(id)
        data = request.get_json()
        item.title = data.get("title", item.title)
        item.content = data.get("content", item.content)
        item.user_id = data.get("user_id", item.user_id)
        db.session.add(item)
        db.session.commit()
        return message_schema.dump(item)

    def delete(self, id):
        item = Message.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {}, 204


class WallResource(Resource):
    def get(self):
        data = Message.query.all() # []
        return messages_basic_schema.dump(data)


class UsersIDMessagesResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        data = Message.query.filter_by(user = user).all()
        return messages_basic_schema.dump(data)

    def post(self, user_id):
        print("-")


api.add_resource(IndexResource, "/")
api.add_resource(UsersResource, "/users/")
api.add_resource(UsersIDResource, "/users/<int:id>")
api.add_resource(WallResource, "/wall/")
api.add_resource(MessagesResource, "/messages/")
api.add_resource(MessagesIDResource, "/messages/<int:id>")
api.add_resource(UsersIDMessagesResource, "/users/<user_id>/messages/")


# LABORATORIO
# que funcione el POST en /users/<user_id>/messages/