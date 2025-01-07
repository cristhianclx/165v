from flask import Flask, render_template, request, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Room(db.Model):

    __tablename__ = "rooms"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Room: {}>".format(self.id)


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    room_id = db.Column(db.String, db.ForeignKey("rooms.id"))
    room = db.relationship("Room", backref="room")

    def __repr__(self):
        return "<Message: {}>".format(self.id)


class MessageSchema(ma.Schema):
    class Meta:
        model = Message
        fields = (
            "id",
            "user",
            "content",
            "priority",
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
    data = Room.query.all()
    new_data = []
    for i in data:
        new_data.append({
            "n": len(Message.query.filter_by(room = i).all()),
            "data": i,
        })
    return render_template("rooms.html", items=new_data)


@app.route("/rooms/create/", methods=["GET", "POST"])
def rooms_create():
    if request.method == "GET":
        return render_template("rooms-create.html")
    if request.method == "POST":
        item = Room(**request.form)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('rooms_by_id', id=item.id))


@app.route("/rooms/<id>/")
def rooms_by_id(id):
    room = Room.query.get_or_404(id)
    messages = Message.query.filter_by(room=room)
    return render_template("messages.html", room=room, messages=messages)


@socketio.on("ws-messages")
def handle_ws_messages(data):
    print("ws-messages: " + str(data))
    item = Message(**data)
    db.session.add(item)
    db.session.commit()
    raw = message_schema.dump(item)
    channel_id = "ws-messages-{}".format(item.room.id)
    socketio.emit(channel_id, raw)