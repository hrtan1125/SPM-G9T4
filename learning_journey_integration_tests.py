import unittest
import flask_testing
import json
# from learning_journey import app, db, Learning_Journey, Learning_Journey_Courses, Courses
from learning_journey import app, db, Learning_Journey, Learning_Journey_Courses, Courses
# from skills import Course_skills
from skills import db as skill_db, Course_skills

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

#viewAllCourses()
class TestViewAllCourses(TestApp):
    def test_view_all_courses(self):
        c1 = Courses(course_id="COR001", course_name="Systems Thinking and Design", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
        c2 = Courses(course_id="COR002", course_name="Lean Six Sigma Green Belt Certification", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
        c3 = Courses(course_id="COR004", course_name="Service Excellence", course_desc="Course description here", course_status="Pending", course_type="Internal", course_category="Core")
        c4 = Courses(course_id="COR006", course_name="Manage Change", course_desc="Course description here", course_status="Retired", course_type="External", course_category="Core")

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.add(c4)
        db.session.commit()

        response = self.client.get("/viewAllCourses", content_type="application/json")

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
            "data": [
                {
                    "course_id":"COR001",
                    "course_name":"Systems Thinking and Design",
                    "course_desc":"Course description here",
                    "course_status":"Active",
                    "course_type":"Internal",
                    "course_category":"Core"
                },
                {
                    "course_id":"COR002",
                    "course_name":"Lean Six Sigma Green Belt Certification",
                    "course_desc":"Course description here",
                    "course_status":"Active",
                    "course_type":"Internal",
                    "course_category":"Core"
                }
            ]
        })
    def test_view_all_courses_with_no_courses(self):
        
        response = self.client.get("/viewAllCourses", content_type="application/json")

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "No courses available."
        })

#remove Courses
class TestRemoveCourses(TestApp):
    def test_remove_courses(self):
        ljc1 = Learning_Journey_Courses(lj_id=1,skill_code="TRM004",course_id="tch009")
        
        db.session.add(ljc1)
        db.session.commit()

        request_body = {
            'lj_id': 1,
            'course': "tch009"
        }
        response = self.client.delete("/removecourses",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
                    "message": "tch009 have been successfully removed."           
        })
#view courses
# class TestViewCourses(TestApp):
#     def test_view_courses(self):
#         cs1 = Course_skills(course_id="COR002", skill_code="GM003")
#         cs2 = Course_skills(course_id="COR006", skill_code="GM003")
#         cs3 = Course_skills(course_id="COR008", skill_code="GM006")

#         c1 = Courses(course_id="COR002", course_name="Lean Six Sigma Green Belt Certification", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
#         c2 = Courses(course_id="COR006", course_name="Manage Change", course_desc="Course description here", course_status="Retired", course_type="Internal", course_category="Core")
#         c3 = Courses(course_id="COR008", course_name="Basic French Certification", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
        
#         skill_db.session.add(cs1)
#         skill_db.session.add(cs2)
#         skill_db.session.add(cs3)
#         db.session.add(c1)
#         db.session.add(c2)
#         db.session.add(c3)
#         db.session.commit()
        
#         response = self.client.get("/viewCourses?skill_code=GM003",
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code,200)
#         self.assertDictEqual(response.json,{
#             "data": [
#                 {
#                     "course_id":"COR002",
#                     "course_name":"Lean Six Sigma Green Belt Certification",
#                     "course_desc":"Course description here",
#                     "course_status":"Active",
#                     "course_type":"Internal",
#                     "course_category":"Core"
#                 }
#             ]
#         })

#create learning journey
class TestCreateLearningJourney(TestApp):
    def test_create_learning_journey(self):
        request_body = {
            'title':'Design Engineer Journey',
            'role_id': 3,
            'staff_id': 150166,
            'courses': []
        }
        response = self.client.post("/createlearningjourney",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,201)
        self.assertDictEqual(response.json, {
                    "lj_id": 1,
                    'title':'Design Engineer Journey',
                    'role_id': 3,
                    'staff_id': 150166            
        })
    def test_create_learning_journey_with_incorrect_data_format(self):
        request_body = {
            'title':'Design Engineer Journey',
            'role_id': 3,
            'staff_id': 150166
        }
        response = self.client.post("/createlearningjourney",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,500)
        self.assertDictEqual(response.json, {
                    "message": "Incorrect Data Format."           
        })

#create learning journey courses
class TestCreateLearningJourneyCourses(TestApp):
    def test_create_learning_journey_courses(self):
        request_body = {
            'lj_id': 1,
            'courses': {"COR000":["Software Project Management"]}
        }
        response = self.client.post("/addlearningjourneycourses",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
                    "message": "Courses successfully added!"           
        })


if __name__ == '__main__':
    unittest.main()