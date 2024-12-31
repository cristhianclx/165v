from flask import Flask, request
from flask_restful import Resource, Api

from bs4 import BeautifulSoup
from datetime import datetime
import requests


app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    def get(self):
        return {'status': 'live'}
    

class PokemonResource(Resource):
    def get(self, name):
        raw = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(name))
        data = raw.json()
        abilities = []
        for x in data["abilities"]:
            abilities.append(x["ability"]["name"])
        return {
            "name": name,
            "abilities": abilities,
            "weight": data["weight"],
        }


class ExchangeResource(Resource):
    def get(self, currency):
        if currency == "USD":
            data = requests.get("https://www.sunat.gob.pe/a/txt/tipoCambio.txt")
            raw = data.text
            exchange_data = raw.split("|")
            return {
                "currency": currency,
                "date": exchange_data[0],
                "buy": exchange_data[1],
                "sale": exchange_data[2],
            }
        if currency == "EUR":
            raw = requests.get("https://cuantoestaeldolar.pe/")
            soup = BeautifulSoup(raw.text, 'html.parser')
            exchange_data = soup.find_all("p", class_="ValueQuotation_text___mR_0")
            return {
                "currency": currency,
                "date": datetime.now().date().strftime("%d/%m/%Y"),
                "buy": exchange_data[6].text,
                "sale": exchange_data[7].text,
            }


class GifSearchResource(Resource):
    def post(self): # 5 gif, ["a", "b", "c"]
        search = request.json.get("q")
        data = requests.get("https://api.giphy.com/v1/gifs/search", params = {
            "api_key": "X83afPN6yM1ApKJeId82IiUP92scDMlM",
            "q": search,
            "limit": 5
        })
        print(data.json())
        return [] # [ { url: "", title: ""},  { url: "", title: ""}, .. ]


api.add_resource(IndexResource, '/')
api.add_resource(PokemonResource, '/pokemon/<name>')
api.add_resource(ExchangeResource, '/exchange/<currency>')
api.add_resource(GifSearchResource, '/gif/search')