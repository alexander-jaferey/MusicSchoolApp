### imports

from os import getenv

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

### config

load_dotenv()
db_url = getenv("DB_URL")
test_db_url = getenv("TEST_DB_URL")
auth0_domain = getenv("AUTH0_DOMAIN")
api_audience = getenv("API_AUDIENCE")

# app = Flask("music-school-api")
# app.config["SQLALCHEMY_DATABASE_URI"] = db_url

# db = SQLAlchemy(app)
