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
        res = self.client().delete("/instruments/17", headers={"Authorization": f"Bearer {jwt}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])
        

    # test for auth failure when deleting individual instrument with no header
    def test_401_no_auth_header_delete_instrument(self):
        res = self.client().delete("/instruments/7")
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
        res = self.client().delete("/instructors/19", headers={"Authorization": f"Bearer {jwt}"})
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
        res = self.client().delete("/courses/20", headers={"Authorization": f"Bearer {jwt}"})
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


    # test posting instrument with authentication
    def test_post_instrument(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().post(
            "/instruments", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={"instrument": "Violin"}
        )
        data = json.loads(res.data)
        instrument = db.session.execute(db.select(Instrument).where(Instrument.instrument == "Violin")).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["id"])
        self.assertTrue(instrument)


    # test for auth failure when posting instrument with no header
    def test_401_no_auth_header_post_instrument(self):
        res = self.client().post("instruments", json={"instrument": "Violin"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])


    # test for auth failure when posting instrument with insufficient permissions
    def test_403_insufficient_permissions_post_instrument(self):
        jwt = getenv("STUDENT_JWT")
        res = self.client().post(
            "/instruments", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={"instrument": "Viola"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])


    # test posting instructor with authentication
    def test_post_instructor(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().post(
            "/instructors", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "first_name": "Thom", 
                "last_name": "Yorke", 
                "workdays": ["Sun", "Tue", "Fri", "Sat"], 
                "instruments": ["Vocals", "Piano", "Guitar"]
            }
        )
        data = json.loads(res.data)
        instructor = db.session.execute(db.select(Instructor).where(Instructor.first_name == "Thom" and Instructor.last_name == "Yorke")).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["id"])
        self.assertTrue(instructor)


    # test for auth failure when posting instructor with no header
    def test_401_no_auth_header_post_instructor(self):
        res = self.client().post(
            "/instructors", 
            json={
                "first_name": "Bob", 
                "last_name": "Dylan", 
                "workdays": ["Sun", "Wed", "Fri", "Sat"], 
                "instruments": ["Vocals", "Guitar"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])


    # test for auth failure when posting instructor with insufficient permissions
    def test_403_insufficient_permissions_post_instructor(self):
        jwt = getenv("STUDENT_JWT")
        res = self.client().post(
            "/instructors", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "first_name": "Bob", 
                "last_name": "Dylan", 
                "workdays": ["Sun", "Wed", "Fri", "Sat"], 
                "instruments": ["Vocals", "Guitar"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])


    # test posting course with authentication
    def test_post_course(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().post(
            "/courses", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "title": "Funk Guitar", 
                "instrument": "Guitar", 
                "schedule": ["Mon", "Wed"]
            }
        )
        data = json.loads(res.data)
        course = db.session.execute(db.select(Course).where(Course.name == "Funk Guitar")).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["id"])
        self.assertTrue(course)


    # test for auth failure when posting course with no header
    def test_401_no_auth_header_post_course(self):
        res = self.client().post(
            "/courses", 
            json={
                "title": "Metal Guitar", 
                "instrument": "Guitar", 
                "schedule": ["Mon", "Wed"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])


    # test for auth failure when posting course with insufficient permissions
    def test_403_insufficient_permissions_post_course(self):
        jwt = getenv("STUDENT_JWT")
        res = self.client().post(
            "/courses", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "title": "Metal Guitar", 
                "instrument": "Guitar", 
                "schedule": ["Mon", "Wed"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])

    
    # test patching instrument with authentication
    def test_patch_instrument(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().patch(
            "/instruments/5", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "new_instructors": ["Steve Martin"], 
                "removed_instructors": ["Jimi Hendrix"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    # test for auth failure when patching instrument with no header
    def test_401_no_auth_header_patch_instrument(self):
        res = self.client().patch(
            "/instruments/5", 
            json={
                "new_instructors": ["Tina Weymouth"], 
                "removed_instructors": ["Ringo Starr"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    
    # test for auth failure when patching instrument with insufficient permissions
    def test_403_insufficient_permissions_patch_instrument(self):
        jwt = getenv("STUDENT_JWT")
        res = self.client().patch(
            "/instruments/5", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "new_instructors": ["Tina Weymouth"], 
                "removed_instructors": ["Ringo Starr"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])


    # test patching instructor with authentication
    def test_patch_instructor(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().patch(
            "/instructors/7", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "new_instruments": ["Vocals"] 
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    # test for auth failure when patching instructor with no header
    def test_401_no_auth_header_patch_instructor(self):
        res = self.client().patch(
            "/instructors/1", 
            json={
                "new_instruments": ["Vocals"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    
    # test for auth failure when patching instructor with insufficient permissions
    def test_403_insufficient_permissions_patch_instructor(self):
        jwt = getenv("STUDENT_JWT")
        res = self.client().patch(
            "/instructors/1", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "new_instruments": ["Vocals"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])
    
    
    # test patching course with authentication
    def test_patch_course(self):
        jwt = getenv("ADMIN_JWT")
        res = self.client().patch(
            "/courses/14", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "new_instructors": ["Jimi Hendrix"], 
                "removed_instructors": ["Ringo Starr"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    # test for auth failure when patching course with no header
    def test_401_no_auth_header_patch_course(self):
        res = self.client().patch(
            "/courses/14", 
            json={
                "new_instructors": ["Kim Deal"], 
                "removed_instructors": ["Ian Anderson"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertTrue(data["message"])

    
    # test for auth failure when patching course with insufficient permissions
    def test_403_insufficient_permissions_patch_course(self):
        jwt = getenv("STUDENT_JWT")
        res = self.client().patch(
            "/courses/14", 
            headers={"Authorization": f"Bearer {jwt}"}, 
            json={
                "new_instructors": ["Kim Deal"], 
                "removed_instructors": ["Ian Anderson"]
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 403)
        self.assertTrue(data["message"])


if __name__ == "__main__":
    unittest.main()