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