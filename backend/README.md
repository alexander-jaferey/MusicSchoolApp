# MusicSchoolApp Backend

## Getting Started

The MusicSchoolApp backend API uses a Python 3 Flask API to communicate with a PostgreSQL database. The main dependencies follow:

* Python 3
* Pip (virtual environment recommended)
* PostgreSQL

### Setup

#### **Database**

Create your database with `createdb`. From the backend directory, `cd` into the db directory and run `psql -d [DATABASE NAME] < db-init.sql` to set up the relations, optionally running `psql -d [DATABASE NAME] < db-data.sql` to populate the database with sample data.

#### **Flask Server**

From the backend directory, setup your virtual environment and run `pip3 install -r requirements.txt` to install the Python dependencies. Copy `.env.example` to `.env` and fill in your environment variables (see the [Auth0 docs](https://auth0.com/docs/get-started) for information on how to set up an Auth0 account and application). Run `python3 main.py` to start the server in development mode on port 5000 on all available addresses.

<br>

___

## Testing

`tests.py` contains a full Python Unittest suite of tests for all available API functions. To run tests, update the `TEST_DB_URL` and JWT variables in `.env` and execute the following:
```
$ ./db-init.sh
$ python3 tests.py
```
`db-init.sh` is a shell script that will create a database with the name `musicschool-test` and populate it with data using `db-test.sql`. Note that `db-test.sql` will prep the database for the user `postgres`, but the database user can be changed by editing the file.

<br>

___

## API Reference

See the [API Reference document](api-reference.md) for detailed information on API endpoints.