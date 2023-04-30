### imports

from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

### config

db_url = getenv("DB_URL")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db = SQLAlchemy(app)
