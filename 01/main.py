from flask import Flask, request
from bs4 import BeautifulSoup
from datetime import datetime
from spellchecker import SpellChecker
import requests

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

@app.route("/exchange-rate/")
def get_exchange_rate():
    # USD
    data_USD = requests.get("https://www.sunat.gob.pe/a/txt/tipoCambio.txt")
    raw_USD = data_USD.text
    exchange_data_raw_USD = raw_USD.split("|")
    exchange_data_USD = {
        "buy": exchange_data_raw_USD[1],
        "sale": exchange_data_raw_USD[2],
    }
    # EUR
    raw_EUR = requests.get("https://cuantoestaeldolar.pe/")
    soup = BeautifulSoup(raw_EUR.text, 'html.parser')
    exchange_data_raw_EUR = soup.find_all("p", class_="ValueQuotation_text___mR_0")
    exchange_data_EUR = {
        "buy": exchange_data_raw_EUR[6].text,
        "sale": exchange_data_raw_EUR[7].text,
    }
    return {
        "date": datetime.now().date().strftime("%d/%m/%Y"),
        "USD": exchange_data_USD,
        "EUR": exchange_data_EUR,
    }

@app.route("/fix-text/", methods=["POST"])
def fix_text():
    spell = SpellChecker()
    data = request.get_json()
    q = data.get("q")
    new_q = []
    for s in q.split(" "):
        new_q.append(spell.correction(s))
    return {
        "text": " ".join(new_q)
    }