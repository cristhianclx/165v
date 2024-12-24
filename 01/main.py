from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "<p>Hello, World! in Lima</p>"

@app.route("/status/")
def status():
    return {
        "status": "ok"
    }

@app.route("/users/")
def users():
    return [{
        "id": 1,
        "name": "cristhian"
    }, {
        "id": 2,
        "name": "cibertec"
    }]

@app.route("/users/<name>")
def users_by_name(name):
    return "<p>Hello, {} in Lima</p>".format(name)