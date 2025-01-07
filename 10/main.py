from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "user",
            "content",
            "created_at",
        )
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_schema = MessageSchema()
messages_schema = MessageSchema(many = True)


@app.route("/status/")
def status():
    return {
        "status": "live"
    }


@app.route("/")
def index():
    data = Message.query.all()
    return render_template("index.html", items=data)


@socketio.on("ws-welcome")
def handle_ws_welcome(data):
    print("ws-welcome: " + str(data))


@socketio.on("ws-messages")
def handle_ws_messages(data):
    print("ws-messages: " + str(data))
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    information = message_schema.dump(item)
    socketio.emit("ws-messages-responses", information)


# LABORATORIO
# model Message, incluir los campos instructions (texto), y el campo priority (low, high)
# incluir los campos instructions y priority en el html
# si el campo priority es high de algun modo resaltarlo
#    <p>
#    <p style="color: red">
# html, incluir tambien la fecha