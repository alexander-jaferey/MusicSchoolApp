import unittest
import json
from os import getenv

from main import create_app, db
from config import test_db_url
from db.models import Instructor, Course, Instrument

class Tests(unittest.TestCase):
    def setUp(self):
        # testing config and initiaization
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": test_db_url
        })

        self.client = self.app.test_client

    def tearDown(self):
        pass


    # test getting full list of instruments
    def test_get_instruments(self):
        res = self.client().get("/instruments")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["instruments"]))
        self.assertTrue(data["total_instruments"])
        self.assertTrue(data["current_page"])
        self.assertTrue(data["total_pages"])

    # test getting full list of instructors
    def test_get_instructors(self):
        res = self.client().get("/instructors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["instructors"]))
        self.assertTrue(data["total_instructors"])
        self.assertTrue(data["current_page"])
        self.assertTrue(data["total_pages"])

    # test getting full list of courses
    def test_get_courses(self):
        res = self.client().get("/courses")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["courses"]))
        self.assertTrue(data["total_instruments"])
        self.assertTrue(data["current_page"])
        self.assertTrue(data["total_pages"])

    # test getting individual instrument info with authentication
    def test_get_individual_instrument(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().get("/instruments/1", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["instrument id"])
        self.assertTrue(data["instrument"])
        self.assertTrue(len(data["instructors"]))
        self.assertTrue(len(data["courses"]))

    # test for auth failure when getting individual instrument with no header
    def test_401_no_auth_header_get_individual_instrument(self):
        res = self.client().get("/instruments/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])


    # test getting individual instructor info with authentication
    def test_get_individual_instructor(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().get("/instructors/1", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["instructor id"])
        self.assertTrue(data["name"])
        self.assertTrue(len(data["workdays"]))
        self.assertTrue(data["instruments"])
        self.assertTrue(data["courses taught"])


    # test for auth failure when getting individual instructor with no header
    def test_401_no_auth_header_get_individual_instructor(self):
        res = self.client().get("/instructors/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])
        

    # test getting individual course info with authentication
    def test_get_individual_course(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().get("/courses/1", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["id"])
        self.assertTrue(data["course title"])
        self.assertTrue(data["instrument"])
        self.assertTrue(len(data["schedule"]))
        self.assertTrue(data["instructors"])


    # test for auth failure when getting individual course with no header
    def test_401_no_auth_header_get_individual_course(self):
        res = self.client().get("/courses/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])


    # test deleting instrument with authentication
    def test_delete_instrument(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().delete("/instruments/2", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])
        

    # test for auth failure when deleting individual instrument with no header
    def test_401_no_auth_header_delete_instrument(self):
        res = self.client().delete("/instruments/5")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    
    # test for auth failure when deleting individual instrument with insufficient permissions
    def test_403_insufficient_permissions_delete_instrument(self):
        jwt = getenv("INSTRUCTOR_JWT")
        res = self.client().delete("/instruments/3", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])

    
    # test deleting instructor with authentication
    def test_delete_instructor(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().delete("/instructors/6", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])
        

    # test for auth failure when deleting individual instructor with no header
    def test_401_no_auth_header_delete_instructor(self):
        res = self.client().delete("/instructors/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    
    # test for auth failure when deleting individual instrument with insufficient permissions
    def test_403_insufficient_permissions_delete_instructor(self):
        jwt = getenv("INSTRUCTOR_JWT")
        res = self.client().delete("/instructors/4", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])

    
    # test deleting course with authentication
    def test_delete_course(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().delete("/courses/4", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])
        

    # test for auth failure when deleting individual course with no header
    def test_401_no_auth_header_delete_course(self):
        res = self.client().delete("/courses/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    
    # test for auth failure when deleting individual instrument with insufficient permissions
    def test_403_insufficient_permissions_delete_course(self):
        jwt = getenv("INSTRUCTOR_JWT")
        res = self.client().delete("/courses/5", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])

if __name__ == "__main__":
    unittest.main()