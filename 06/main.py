from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


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


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title = String(120)
    # content = Text

    # user_id = fk
    # user = relation
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class IndexResource(Resource):
    def get(self):
        return {
            "status": "working"
        }


class UsersResource(Resource):
    def get(self):
        data = User.query.all()
        items = []
        for d in data:
            items.append({
                "id": d.id,
                "name": d.name,
                "age": d.age,
                "country": d.country,
                "city": d.city,
                "address": d.address,
                "language": d.language,
            })
        return items

    def post(self):
        data = request.get_json()
        item = User(**data)
        db.session.add(item)
        db.session.commit()
        return {
            "id": item.id,
            "name": item.name,
            "age": item.age,
            "country": item.country,
            "city": item.city,
            "address": item.address,
            "language": item.language,
        }, 201


api.add_resource(IndexResource, "/")
api.add_resource(UsersResource, "/users/")

# LABORATORIO
# (1) modelo message, completarlo
# (2) migration
# (3) URL /messages/, GET, POST