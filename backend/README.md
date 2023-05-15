# MusicSchoolApp Backend

## Getting Started
___

The MusicSchoolApp backend API uses a Python 3 Flask API to communicate with a PostgreSQL database. The main dependencies follow:

* Python 3
* Pip (virtual environment recommended)
* PostgreSQL

### Setup

#### **Database**

Create your database and, from the backend directory, run `psql -d [DATABASE NAME] < db-init.sql` to set up the relations, replacing `db-init.sql` with `db-sample-data.sql` to additionally populate the database with sample data.

#### **Flask Server**

From the backend directory, setup your virtual environment and run `pip3 install -r requirements.txt` to install the Python dependencies. Copy `.env.example` to `.env` and fill in your environment variables (see the [Auth0 docs](https://auth0.com/docs/get-started) for information on how to set up an Auth0 account and application). Run `python3 main.py` to start the server in development mode on port 5000 on all available addresses.

<br>

## Testing
___

**TODO**

<br>

## API Reference
___

**TODO**