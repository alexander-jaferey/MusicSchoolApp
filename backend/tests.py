import unittest
import json
from os import getenv

from flask_sqlalchemy import SQLAlchemy

from main import app, db
from db.models import Instructor, Course, Instrument

class Tests(unittest.TestCase):
    def setUp(self):
        # testing config and initiaization
        self.app = app
        self.client = self.app.test_client
        self.database_path = getenv("TEST_DB_URL")

        self.app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        with self.app.app_context():
            self.db = db

    def tearDown(self):
        pass



    def test_get_instruments(self):
        res = self.client().get("/instruments")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["instruments"]))
        self.assertTrue(data["total_instruments"])
        self.assertTrue(data["current_page"])
        self.assertTrue(data["total_pages"])

    def test_get_instructors(self):
        res = self.client().get("/instructors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["instructors"]))
        self.assertTrue(data["total_instructors"])
        self.assertTrue(data["current_page"])
        self.assertTrue(data["total_pages"])

    def test_get_courses(self):
        res = self.client().get("/courses")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["courses"]))
        self.assertTrue(data["total_instruments"])
        self.assertTrue(data["current_page"])
        self.assertTrue(data["total_pages"])


if __name__ == "__main__":
    unittest.main()