# https://www.python.org/downloads/

# commands

# virtualenv

python -m venv .venv
.venv\Scripts\activate.bat # activate.ps

# activate virtualenv

.venv\Scripts\activate.bat # activate.ps

# install

pip install -r requirements.txt --upgrade

# utils

pip freeze
pip install flask

# flask

flask --app main run --reload

# database

flask --app main db init # init
flask --app main db migrate # create migration
flask --app main db upgrade # apply migration
flask --app main db downgrade # revert migration

# shell

flask --app main shell

>>> import csv
>>> rows = []
>>> with open("jokes.csv") as csv_file:
...     csv_reader = csv.reader(csv_file)
...     header = next(csv_reader)
...     for row in csv_reader:
...         rows.append(row)
...
>>> from main import db, Joke
>>> for row in rows:
...     joke = Joke(
...         routine_id = int(row[0]),
...         show_id = int(row[1]),
...         event_name = row[2],
...         show_name = row[3],
...         start_timestamp = row[4],
...         text = row[5],
...         video_id = row[6],
...     )
...     db.session.add(joke)
...     db.session.commit()
... 