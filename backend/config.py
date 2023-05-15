### imports

from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

### config

load_dotenv()
db_url = getenv("DB_URL")

app = Flask("music-school-api")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db = SQLAlchemy(app)
