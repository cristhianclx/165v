from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id) # "<User: 1>"
    

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message: {}>".format(self.id) # "<Message: 1>"


@app.route("/status/")
def status():
    return {
        "status": "live"
    }


@app.route("/users/")
def users():
    data = User.query.all()    
    return render_template("users.html", items=data)


@app.route("/users/add/", methods=["GET", "POST"])
def users_add():
    if request.method == "GET":
        return render_template("users-add.html")
    if request.method == "POST":
        item = User(
            first_name=request.form.get("first_name"),
            last_name=request.form.get("last_name"),
            age=request.form.get("age"),
            country=request.form.get("country"),
            city=request.form.get("city"),
        )
        db.session.add(item)
        db.session.commit()
        return render_template("users-add.html", info="User added")
    

@app.route("/users/<id>")
def users_by_id(id):
    data = User.query.get_or_404(id)
    return render_template("users-details.html", item=data)


@app.route("/messages/")
def messages():
    data = Message.query.all()    
    return render_template("messages.html", items=data)


@app.route("/messages/add/", methods=["GET", "POST"])
def messages_add():
    if request.method == "GET":
        return render_template("messages-add.html")
    if request.method == "POST":
        item = Message(
            title=request.form.get("title"),
            content=request.form.get("content"),
            user_id=request.form.get("user_id"),
        )
        db.session.add(item)
        db.session.commit()
        return render_template("messages-add.html", info="Message added")