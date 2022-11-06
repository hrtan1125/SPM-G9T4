import unittest
import flask_testing
import json
# from learning_journey import app, db, Learning_Journey, Learning_Journey_Courses, Courses
from learning_journey import app, db, Learning_Journey, Learning_Journey_Courses, Courses, Staff, Registration
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
class TestViewCourses(TestApp):
    def test_view_courses(self):
        cs1 = Course_skills(course_id="COR002", skill_code="GM003")
        cs2 = Course_skills(course_id="COR006", skill_code="GM003")
        cs3 = Course_skills(course_id="COR008", skill_code="GM006")

        c1 = Courses(course_id="COR002", course_name="Lean Six Sigma Green Belt Certification", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
        c2 = Courses(course_id="COR006", course_name="Manage Change", course_desc="Course description here", course_status="Retired", course_type="Internal", course_category="Core")
        c3 = Courses(course_id="COR008", course_name="Basic French Certification", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
        
        db.session.add(cs1)
        db.session.add(cs2)
        db.session.add(cs3)
        

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.commit()
        
        response = self.client.get("/viewCourses?skill_code=GM003",
                                    content_type='application/json')
        
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
            "data": [
                {
                    "course_id":"COR002",
                    "course_name":"Lean Six Sigma Green Belt Certification",
                    "course_desc":"Course description here",
                    "course_status":"Active",
                    "course_type":"Internal",
                    "course_category":"Core"
                }]
        })

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

class TestAdminViewLearners(TestApp):
    def test_admin_view_learners(self):
        s1 = Staff(Staff_ID=130001,Staff_FName="John",Staff_LName="Sim",Dept="Chariman",Email="john.sim@allinone.com.sg",Role=1)
        s2 = Staff(Staff_ID=130002,Staff_FName="Jack",Staff_LName="Sim",Dept="CEO",Email="jack.sim@allinone.com.sg",Role=1)
        s3 = Staff(Staff_ID=130003,Staff_FName="Jack",Staff_LName="Ma",Dept="Sales",Email="jack.ma@allinone.com.sg",Role=1)

        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        response = self.client.get("/AdminViewLearners?staff_id=130001",
                                    content_type='application/json')
        
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
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
            "Email": "jack.ma@allinone.com.sg",
            "Role": 1,
            "Staff_FName": "Jack",
            "Staff_ID": 130003,
            "Staff_LName": "Ma"
        }]
        })
    def test_adminViewLearners_missing_id(self):
        s1 = Staff(Staff_ID=130001, Staff_FName="John", Staff_LName = "Sim", Dept = "Chairman", Email = "jack.sim@allinone.com.sg", Role = 1)
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/AdminViewLearners",
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "There are no learners available"
        }) 

class testCheckRoles(TestApp):
    def test_check_role(self):
        s1 = Staff(Staff_ID=130001, Staff_FName="John", Staff_LName = "Sim", Dept = "Chairman", Email = "jack.sim@allinone.com.sg", Role = 1)
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'staff_id':130001
        }

        response = self.client.get("/checkrole",
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

        response = self.client.get("/checkrole?staff_id=999999",
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Invalid staff ID!"
        })

class testViewTeamMembers(TestApp):
    def test_view_team_member(self):
        s1 = Staff(Staff_ID=140001, Staff_FName="Derek", Staff_LName = "Tan", Dept = "Sales", Email = "Derek.Tan@allinone.com.sg", Role = 3)
        s2 = Staff(Staff_ID=140002, Staff_FName="Susan", Staff_LName = "Goh", Dept = "Sales", Email = "Susan.Goh@allinone.com.sg", Role = 2)
        s3 = Staff(Staff_ID=140003, Staff_FName="Janice", Staff_LName = "Chan", Dept = "Sales", Email = "Janice.Chan@allinone.com.sg", Role = 2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()


        response = self.client.get("/viewTeamMembers?dept=Sales&staff_id=140001",
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
            }
        ]
    })

    def test_view_team_members_missing_input(self):
        s1 = Staff(Staff_ID=140001, Staff_FName="Derek", Staff_LName = "Tan", Dept = "Sales", Email = "Derek.Tan@allinone.com.sg", Role = 3)
        db.session.add(s1)
        db.session.commit()

        response = self.client.get("/viewTeamMembers",
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Missing Input."
        })

class TestRegistration(TestApp):
    def test_registration(self):
        r1 = Registration(reg_id=1,course_id="COR002",staff_id=130001,reg_status="Registered",completion_status="Completed")
        r2 = Registration(reg_id=2,course_id="COR002",staff_id=130002,reg_status="Registered",completion_status="Completed")
        r3 = Registration(reg_id=3,course_id="COR002",staff_id=140001,reg_status="Registered",completion_status="Completed")
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()
        response = self.client.get("/viewAllRegistration",
                                    content_type='application/json')
        
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
        "data": [
        {
            "completion_status": "Completed",
            "course_id": "COR002",
            "reg_id": 1,
            "reg_status": "Registered",
            "staff_id": 130001
        },
        {
            "completion_status": "Completed",
            "course_id": "COR002",
            "reg_id": 2,
            "reg_status": "Registered",
            "staff_id": 130002
        },
        {
            "completion_status": "Completed",
            "course_id": "COR002",
            "reg_id": 3,
            "reg_status": "Registered",
            "staff_id": 140001
        }]
        })

class TestViewCoursesByLearningJourney(TestApp):
    def test_view_courses_by_learningjourney(self):
        lj1 = Learning_Journey(lj_id=1, title="Learning Journey 1",role_id=3,staff_id=170166)
        # lj2 = Learning_Journey(lj_id=1, title="My Learning Journey",role_id=1,staff_id=150166)
        # lj3 = Learning_Journey(lj_id=1, title="Be CEO in Future",role_id=8,staff_id=150166)
        c1 = Courses(course_id="tch009",course_name="Systems Thinking and Design",course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",course_status="Active",course_type="Internal",course_category="Core")
        c2 = Courses(course_id="tch012",course_name="Lean Six Sigma Green Belt Certification",course_desc="Apply Lean Six Sigma methodology and statistical tools such as Minitab to be used in process analytics",course_status="Active",course_type="Internal",course_category="Core")
        c3 = Courses(course_id="tch015",course_name="Service Excellence",course_desc="The programme provides the learner with the key foundations of what builds customer confidence in the service industr",course_status="Pending",course_type="Internal",course_category="Core")
        ljc1 = Learning_Journey_Courses(row_id=1,lj_id=1,skill_code="TRM004",course_id="tch009")
        ljc2 = Learning_Journey_Courses(row_id=2,lj_id=1,skill_code="TRM004",course_id="tch012")
        ljc3 = Learning_Journey_Courses(row_id=3,lj_id=1,skill_code="TRM004",course_id="tch015")
        r1 = Registration(reg_id=1,course_id="COR002",staff_id=130001,reg_status="Registered",completion_status="OnGoing")
        r2 = Registration(reg_id=2,course_id="COR002",staff_id=130002,reg_status="Registered",completion_status="OnGoing")
        r3 = Registration(reg_id=3,course_id="COR002",staff_id=140001,reg_status="Registered",completion_status="OnGoing")

        db.session.add(lj1)
        # db.session.add(lj2)
        # db.session.add(lj3)
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.add(ljc1)
        db.session.add(ljc2)
        db.session.add(ljc3)
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()
        response = self.client.get("/viewCoursesByLearningJourney?lj_id=1",
                                    content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,
        {   "courses":{"tch009":{"completion_status":"","course_name":"Systems Thinking and Design"},
            "tch012":{"completion_status":"","course_name":"Lean Six Sigma Green Belt Certification"},
            "tch015":{"completion_status":"","course_name":"Service Excellence"}},
            "progress":0
        })


if __name__ == '__main__':
    unittest.main()