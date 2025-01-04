from flask import Flask, request
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

api = Api(app)


class Joke(db.Model):
    __tablename__ = "jokes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    routine_id = db.Column(db.Integer, nullable=True)
    show_id = db.Column(db.Integer, nullable=True)
    event_name = db.Column(db.String(255), nullable=True)
    show_name = db.Column(db.String(255), nullable=True)
    start_timestamp = db.Column(db.String(8), nullable=True)
    text = db.Column(db.Text)
    video_id = db.Column(db.String(20))

    def __repr__(self):
        return "<Joke: {}>".format(self.id)


class JokeSchema(ma.Schema):
    class Meta:
        model = Joke
        fields = (
            "id",
            "routine_id",
            "show_id",
            "event_name",
            "show_name",
            "start_timestamp",
            "text",
            "video_id",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


joke_schema = JokeSchema()
jokes_schema = JokeSchema(many = True)


class IndexResource(Resource):
    def get(self):
        return {
            "working": "ok"
        }


class JokesResource(Resource):
    def get(self):
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 20))
        data = Joke.query.all()
        return {
            "page": page,
            "count": len(data),
            "results": jokes_schema.dump(data[(page-1)*page_size:page*page_size])
        }


api.add_resource(IndexResource, "/")
api.add_resource(JokesResource, "/jokes/")

# /jokes/ => 2.32 MB
# /jokes/?page=1&page_size=20 => 9 kb