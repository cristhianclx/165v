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

>>> from main import db, User
>>> item = User(name="Alan", age=42, country="PE", city="Lima")
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, User
>>> User.query.all()

>>> from main import db, User
>>> User.query.get_or_404(2)
>>> User.query.filter_by(id=2).first()

>>> from main import db, User
>>> item = User.query.get(2)
>>> item.city = "Huancayo"
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, User
>>> item = User.query.get(2)
>>> db.session.delete(item)
>>> db.session.commit()

>>> from main import db, User, Message
>>> user = User.query.get_or_404(1)
>>> Message.query.filter_by(user = user).all()

# utils

black file.py --diff
black file.py
flake8 file.py