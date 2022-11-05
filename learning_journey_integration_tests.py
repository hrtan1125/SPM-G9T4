import unittest
import flask_testing
import json
# from learning_journey import app, db, Learning_Journey, Learning_Journey_Courses, Courses
from learning_journey import app, db, Learning_Journey, Learning_Journey_Courses, Courses, Staff
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


class testCheckRoles(TestApp):
    def test_check_role(self):
        s1 = Staff(Staff_ID=130001, Staff_FName="John", Staff_LName = "Sim", Dept = "Chairman", Email = "jack.sim@allinone.com.sg", Role = 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'staff_id':130001
        }

        response = self.client.put("/checkrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
            "data": [
                {
                    "role": 1,
                    "dept": "Chairman",
                    "name": "John Sim",
                    "staff_id" : 130001
                }
            ]
        })

    def test_check_role_invalid_id(self):
        s1 = Staff(Staff_ID=130001, Staff_FName="John", Staff_LName = "Sim", Dept = "Chairman", Email = "jack.sim@allinone.com.sg", Role = 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'staff_id':999999
        }

        response = self.client.put("/checkrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Invalid staff ID!"
        })

class testViewTeamMembers(TestApp):
    def test_view_team_member(self):
        s1 = Staff(Staff_ID=140001, Staff_FName="Derek", Staff_LName = "Tan", Dept = "Sales", Email = "Derek.Tan@allinone.com.sg", Role = 3)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'staff_id':140001,
            'dept': "Sales"
        }

        response = self.client.put("/viewTeamMembers",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
        "data": [
            {
                "Dept": "Sales",
                "Email": "Susan.Goh@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Susan",
                "Staff_ID": 140002,
                "Staff_LName": "Goh"
            },
            {
                "Dept": "Sales",
                "Email": "Janice.Chan@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Janice",
                "Staff_ID": 140003,
                "Staff_LName": "Chan"
            },
            {
                "Dept": "Sales",
                "Email": "Mary.Teo@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Mary",
                "Staff_ID": 140004,
                "Staff_LName": "Teo"
            },
            {
                "Dept": "Sales",
                "Email": "Jaclyn.Lee@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Jaclyn",
                "Staff_ID": 140008,
                "Staff_LName": "Lee"
            },
            {
                "Dept": "Sales",
                "Email": "Oliva.Lim@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Oliva",
                "Staff_ID": 140015,
                "Staff_LName": "Lim"
            },
            {
                "Dept": "Sales",
                "Email": "Emma.Heng@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Emma",
                "Staff_ID": 140025,
                "Staff_LName": "Heng"
            },
            {
                "Dept": "Sales",
                "Email": "Charlotte.Wong@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Charlotte",
                "Staff_ID": 140036,
                "Staff_LName": "Wong"
            },
            {
                "Dept": "Sales",
                "Email": "Amelia.Ong@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Amelia",
                "Staff_ID": 140078,
                "Staff_LName": "Ong"
            },
            {
                "Dept": "Sales",
                "Email": "Eva.Yong@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Eva",
                "Staff_ID": 140102,
                "Staff_LName": "Yong"
            },
            {
                "Dept": "Sales",
                "Email": "Sophia.Toh@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Sophia",
                "Staff_ID": 140103,
                "Staff_LName": "Toh"
            },
            {
                "Dept": "Sales",
                "Email": "Liam.The@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Liam",
                "Staff_ID": 140108,
                "Staff_LName": "The"
            },
            {
                "Dept": "Sales",
                "Email": "Noah.Ng@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Noah",
                "Staff_ID": 140115,
                "Staff_LName": "Ng"
            },
            {
                "Dept": "Sales",
                "Email": "Oliver.Tan@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "Oliver",
                "Staff_ID": 140525,
                "Staff_LName": "Tan"
            },
            {
                "Dept": "Sales",
                "Email": "William.Fu@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "William",
                "Staff_ID": 140736,
                "Staff_LName": "Fu"
            },
            {
                "Dept": "Sales",
                "Email": "James.Tong@allinone.com.sg",
                "Role": 2,
                "Staff_FName": "James",
                "Staff_ID": 140878,
                "Staff_LName": "Tong"
            }
        ]
    })

    def test_view_team_members_missing_input(self):
        s1 = Staff(Staff_ID=140001, Staff_FName="Derek", Staff_LName = "Tan", Dept = "Sales", Email = "Derek.Tan@allinone.com.sg", Role = 3)
        db.session.commit(s1)

        request_body = {
            'dept': "Sales"
        }

        response = self.client.put("/viewTeamMembers",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Missing Input."
        })
class testAdminViewLearners(TestApp):
    def test_adminViewLearners(self):
        s1 = Staff(Staff_ID=130001, Staff_FName="John", Staff_LName = "Sim", Dept = "Chairman", Email = "jack.sim@allinone.com.sg", Role = 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'staff_id':130001
        }

        response = self.client.put("/AdminViewLearners",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
            "data": [
                {
                    "Dept": "CEO",
                    "Email": "jack.sim@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Jack",
                    "Staff_ID": 130002,
                    "Staff_LName": "Sim"
                },
                {
                    "Dept": "Sales",
                    "Email": "Derek.Tan@allinone.com.sg",
                    "Role": 3,
                    "Staff_FName": "Derek",
                    "Staff_ID": 140001,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Sales",
                    "Email": "Susan.Goh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Susan",
                    "Staff_ID": 140002,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Sales",
                    "Email": "Janice.Chan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Janice",
                    "Staff_ID": 140003,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Sales",
                    "Email": "Mary.Teo@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Mary",
                    "Staff_ID": 140004,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Sales",
                    "Email": "Jaclyn.Lee@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jaclyn",
                    "Staff_ID": 140008,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Sales",
                    "Email": "Oliva.Lim@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliva",
                    "Staff_ID": 140015,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Sales",
                    "Email": "Emma.Heng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Emma",
                    "Staff_ID": 140025,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "Sales",
                    "Email": "Charlotte.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Charlotte",
                    "Staff_ID": 140036,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Sales",
                    "Email": "Amelia.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Amelia",
                    "Staff_ID": 140078,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Sales",
                    "Email": "Eva.Yong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Eva",
                    "Staff_ID": 140102,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "Sales",
                    "Email": "Sophia.Toh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Sophia",
                    "Staff_ID": 140103,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "Sales",
                    "Email": "Liam.The@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Liam",
                    "Staff_ID": 140108,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "Sales",
                    "Email": "Noah.Ng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Noah",
                    "Staff_ID": 140115,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "Sales",
                    "Email": "Oliver.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliver",
                    "Staff_ID": 140525,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Sales",
                    "Email": "William.Fu@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "William",
                    "Staff_ID": 140736,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "Sales",
                    "Email": "James.Tong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "James",
                    "Staff_ID": 140878,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Eric.Loh@allinone.com.sg",
                    "Role": 3,
                    "Staff_FName": "Eric",
                    "Staff_ID": 150008,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Noah.Goh@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Noah",
                    "Staff_ID": 150065,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Liam.Tan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Liam",
                    "Staff_ID": 150075,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliver.Chan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Oliver",
                    "Staff_ID": 150076,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Michael.Ng@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Michael",
                    "Staff_ID": 150085,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Alexander.The@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Alexander",
                    "Staff_ID": 150095,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "Ops",
                    "Email": "Ethan.Tan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Ethan",
                    "Staff_ID": 150096,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jaclyn.Lee@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Jaclyn",
                    "Staff_ID": 150115,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Ops",
                    "Email": "William.Teo@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "William",
                    "Staff_ID": 150118,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Ops",
                    "Email": "Mary.Teo@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Mary",
                    "Staff_ID": 150125,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliva.Lim@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliva",
                    "Staff_ID": 150126,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Ops",
                    "Email": "Daniel.Fu@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Daniel",
                    "Staff_ID": 150138,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "Ops",
                    "Email": "James.Lee@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "James",
                    "Staff_ID": 150142,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Ops",
                    "Email": "John.Lim@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "John",
                    "Staff_ID": 150143,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jack.Heng@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Jack",
                    "Staff_ID": 150148,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Derek.Wong@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Derek",
                    "Staff_ID": 150155,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jacob.Tong@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Jacob",
                    "Staff_ID": 150162,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Logan.Loh@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Logan",
                    "Staff_ID": 150163,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliver.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliver",
                    "Staff_ID": 150165,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "William.Fu@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "William",
                    "Staff_ID": 150166,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jackson.Tan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Jackson",
                    "Staff_ID": 150168,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Aiden.Tan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Aiden",
                    "Staff_ID": 150175,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Emma.Heng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Emma",
                    "Staff_ID": 150192,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Charlotte.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Charlotte",
                    "Staff_ID": 150193,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Amelia.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Amelia",
                    "Staff_ID": 150198,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Eva.Yong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Eva",
                    "Staff_ID": 150205,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "Ops",
                    "Email": "James.Tong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "James",
                    "Staff_ID": 150208,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Michael.Lee@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Michael",
                    "Staff_ID": 150215,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Ops",
                    "Email": "Ethan.Lim@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Ethan",
                    "Staff_ID": 150216,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Ops",
                    "Email": "John.Loh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "John",
                    "Staff_ID": 150232,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jack.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jack",
                    "Staff_ID": 150233,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Derek.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Derek",
                    "Staff_ID": 150238,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Benjamin.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Benjamin",
                    "Staff_ID": 150245,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Daniel.Heng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Daniel",
                    "Staff_ID": 150258,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jaclyn.Tong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jaclyn",
                    "Staff_ID": 150265,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Mary.Fu@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Mary",
                    "Staff_ID": 150275,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliva.Loh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliva",
                    "Staff_ID": 150276,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jacob.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jacob",
                    "Staff_ID": 150282,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Logan.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Logan",
                    "Staff_ID": 150283,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jackson.Yong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jackson",
                    "Staff_ID": 150288,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Aiden.Toh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Aiden",
                    "Staff_ID": 150295,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Emma.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Emma",
                    "Staff_ID": 150318,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Charlotte.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Charlotte",
                    "Staff_ID": 150342,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Amelia.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Amelia",
                    "Staff_ID": 150343,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "William.Heng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "William",
                    "Staff_ID": 150345,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Eva.Goh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Eva",
                    "Staff_ID": 150348,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Sophia.Chan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Sophia",
                    "Staff_ID": 150355,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Ops",
                    "Email": "James.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "James",
                    "Staff_ID": 150356,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Ops",
                    "Email": "John.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "John",
                    "Staff_ID": 150398,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jack.Yong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jack",
                    "Staff_ID": 150422,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Derek.Toh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Derek",
                    "Staff_ID": 150423,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Benjamin.The@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Benjamin",
                    "Staff_ID": 150428,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "Ops",
                    "Email": "Lucas.Ng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Lucas",
                    "Staff_ID": 150435,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Ethan.Loh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Ethan",
                    "Staff_ID": 150445,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Daniel.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Daniel",
                    "Staff_ID": 150446,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jacob.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jacob",
                    "Staff_ID": 150488,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Logan.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Logan",
                    "Staff_ID": 150512,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jackson.Goh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jackson",
                    "Staff_ID": 150513,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Aiden.Chan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Aiden",
                    "Staff_ID": 150518,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Samuel.Teo@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Samuel",
                    "Staff_ID": 150525,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Ops",
                    "Email": "Jaclyn.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jaclyn",
                    "Staff_ID": 150555,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Benjamin.Ong@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Benjamin",
                    "Staff_ID": 150565,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliva.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliva",
                    "Staff_ID": 150566,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Samuel.Tan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Samuel",
                    "Staff_ID": 150585,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Emma.Yong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Emma",
                    "Staff_ID": 150608,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Sophia.Toh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Sophia",
                    "Staff_ID": 150615,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Charlotte.Toh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Charlotte",
                    "Staff_ID": 150632,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Amelia.The@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Amelia",
                    "Staff_ID": 150633,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "Ops",
                    "Email": "Eva.Ng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Eva",
                    "Staff_ID": 150638,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Sophia.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Sophia",
                    "Staff_ID": 150645,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Lucas.Goh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Lucas",
                    "Staff_ID": 150655,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Ops",
                    "Email": "William.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "William",
                    "Staff_ID": 150695,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Samuel.The@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Samuel",
                    "Staff_ID": 150705,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "Ops",
                    "Email": "Liam.Teo@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Liam",
                    "Staff_ID": 150765,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Ops",
                    "Email": "Lucas.Yong@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Lucas",
                    "Staff_ID": 150776,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Susan.Goh@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Susan",
                    "Staff_ID": 150796,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Liam.The@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Liam",
                    "Staff_ID": 150826,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "Ops",
                    "Email": "Henry.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Henry",
                    "Staff_ID": 150845,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Henry.Chan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Henry",
                    "Staff_ID": 150866,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Susan.Ng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Susan",
                    "Staff_ID": 150916,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Henry.Toh@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Henry",
                    "Staff_ID": 150918,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "Ops",
                    "Email": "Susan.Lee@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Susan",
                    "Staff_ID": 150935,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Ops",
                    "Email": "Janice.Chan@allinone.com.sg",
                    "Role": 4,
                    "Staff_FName": "Janice",
                    "Staff_ID": 150938,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Noah.Ng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Noah",
                    "Staff_ID": 150968,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Noah.Lee@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Noah",
                    "Staff_ID": 150976,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Ops",
                    "Email": "Alexander.Teo@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Alexander",
                    "Staff_ID": 151008,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Ops",
                    "Email": "Liam.Fu@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Liam",
                    "Staff_ID": 151055,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "Ops",
                    "Email": "Alexander.Fu@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Alexander",
                    "Staff_ID": 151056,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "Ops",
                    "Email": "Janice.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Janice",
                    "Staff_ID": 151058,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliver.Lim@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliver",
                    "Staff_ID": 151118,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Ops",
                    "Email": "Janice.Lim@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Janice",
                    "Staff_ID": 151146,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Ops",
                    "Email": "Michael.Tong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Michael",
                    "Staff_ID": 151198,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Noah.Tong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Noah",
                    "Staff_ID": 151266,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "Ops",
                    "Email": "Mary.Heng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Mary",
                    "Staff_ID": 151288,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "Ops",
                    "Email": "Oliver.Loh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliver",
                    "Staff_ID": 151408,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "HR",
                    "Email": "Sally.Loh@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Sally",
                    "Staff_ID": 160008,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "HR",
                    "Email": "John.Tan@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "John",
                    "Staff_ID": 160065,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "HR",
                    "Email": "James.Tan@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "James",
                    "Staff_ID": 160075,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "HR",
                    "Email": "Jack.Goh@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Jack",
                    "Staff_ID": 160076,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "HR",
                    "Email": "Derek.Chan@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Derek",
                    "Staff_ID": 160118,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "HR",
                    "Email": "Jaclyn.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jaclyn",
                    "Staff_ID": 160135,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "HR",
                    "Email": "Benjamin.Teo@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Benjamin",
                    "Staff_ID": 160142,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "HR",
                    "Email": "Lucas.Lee@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Lucas",
                    "Staff_ID": 160143,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "HR",
                    "Email": "Mary.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Mary",
                    "Staff_ID": 160145,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "HR",
                    "Email": "Oliva.Yong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Oliva",
                    "Staff_ID": 160146,
                    "Staff_LName": "Yong"
                },
                {
                    "Dept": "HR",
                    "Email": "Henry.Lim@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Henry",
                    "Staff_ID": 160148,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "HR",
                    "Email": "Alexander.Heng@allinone.com.sg",
                    "Role": 1,
                    "Staff_FName": "Alexander",
                    "Staff_ID": 160155,
                    "Staff_LName": "Heng"
                },
                {
                    "Dept": "HR",
                    "Email": "Emma.Toh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Emma",
                    "Staff_ID": 160188,
                    "Staff_LName": "Toh"
                },
                {
                    "Dept": "HR",
                    "Email": "Charlotte.The@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Charlotte",
                    "Staff_ID": 160212,
                    "Staff_LName": "The"
                },
                {
                    "Dept": "HR",
                    "Email": "Amelia.Ng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Amelia",
                    "Staff_ID": 160213,
                    "Staff_LName": "Ng"
                },
                {
                    "Dept": "HR",
                    "Email": "Eva.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Eva",
                    "Staff_ID": 160218,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "HR",
                    "Email": "Sophia.Fu@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Sophia",
                    "Staff_ID": 160225,
                    "Staff_LName": "Fu"
                },
                {
                    "Dept": "HR",
                    "Email": "Michael.Tong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Michael",
                    "Staff_ID": 160258,
                    "Staff_LName": "Tong"
                },
                {
                    "Dept": "HR",
                    "Email": "Ethan.Loh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Ethan",
                    "Staff_ID": 160282,
                    "Staff_LName": "Loh"
                },
                {
                    "Dept": "Finance",
                    "Email": "David.Yap@allinone.com.sg",
                    "Role": 3,
                    "Staff_FName": "David",
                    "Staff_ID": 170166,
                    "Staff_LName": "Yap"
                },
                {
                    "Dept": "Finance",
                    "Email": "Daniel.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Daniel",
                    "Staff_ID": 170208,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Finance",
                    "Email": "Mary.Wong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Mary",
                    "Staff_ID": 170215,
                    "Staff_LName": "Wong"
                },
                {
                    "Dept": "Finance",
                    "Email": "Jaclyn.Ong@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jaclyn",
                    "Staff_ID": 170216,
                    "Staff_LName": "Ong"
                },
                {
                    "Dept": "Finance",
                    "Email": "Jacob.Tan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jacob",
                    "Staff_ID": 170232,
                    "Staff_LName": "Tan"
                },
                {
                    "Dept": "Finance",
                    "Email": "Logan.Goh@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Logan",
                    "Staff_ID": 170233,
                    "Staff_LName": "Goh"
                },
                {
                    "Dept": "Finance",
                    "Email": "Jackson.Chan@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Jackson",
                    "Staff_ID": 170238,
                    "Staff_LName": "Chan"
                },
                {
                    "Dept": "Finance",
                    "Email": "Aiden.Teo@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Aiden",
                    "Staff_ID": 170245,
                    "Staff_LName": "Teo"
                },
                {
                    "Dept": "Finance",
                    "Email": "Samuel.Lee@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Samuel",
                    "Staff_ID": 170655,
                    "Staff_LName": "Lee"
                },
                {
                    "Dept": "Finance",
                    "Email": "Susan.Lim@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Susan",
                    "Staff_ID": 170866,
                    "Staff_LName": "Lim"
                },
                {
                    "Dept": "Finance",
                    "Email": "Janice.Heng@allinone.com.sg",
                    "Role": 2,
                    "Staff_FName": "Janice",
                    "Staff_ID": 171008,
                    "Staff_LName": "Heng"
                }
            ]
        })

    def test_adminViewLearners_missing_id(self):
        s1 = Staff(Staff_ID=130001, Staff_FName="John", Staff_LName = "Sim", Dept = "Chairman", Email = "jack.sim@allinone.com.sg", Role = 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'staff_id': ""
        }

        response = self.client.put("/AdminViewLearners",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "There are no learners available"
        })


if __name__ == '__main__':
    unittest.main()