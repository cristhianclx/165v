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