import unittest
from learning_journey import Learning_Journey, Registration, Staff, Learning_Journey_Courses, Courses

class TestLearningJourney(unittest.TestCase):
    def setUp(self):
        self.lj1 = Learning_Journey(lj_id=1, title="Learning Journey 1", role_id="3", staff_id="170166")
        self.lj2 = Learning_Journey(lj_id=2, title="My Learning Journey", role_id="1", staff_id="150166")

    def tearDown(self):
        self.lj1 = None
        self.lj2 = None

    def test_to_dict(self):
        result = self.lj1.to_dict()
        self.assertEqual(result, {
            'lj_id': 1,
            'title': 'Learning Journey 1',
            'role_id': '3',
            'staff_id': '170166'}
        )

class TestLearningJourneyCourses(unittest.TestCase):
    def setUp(self):
        self.lj_course = Learning_Journey_Courses(lj_id=1,skill_code="TRM004",course_id="tch012")

    def tearDown(self):
        self.lj_course = None

    def test_to_dict(self):
        self.assertDictEqual(self.lj_course.to_dict(),{
            "row_id":None,
            "lj_id": 1,
            "skill_code":"TRM004",
            "course_id": "tch012"
        })

class TestCourses(unittest.TestCase):
    def setUp(self):
        self.course = Courses(course_id="COR001",course_name="Systems Thinking and Design",course_desc="This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",course_status="Active",course_type="Internal",course_category="Core")

    def tearDown(self):
        self.course = None

    def test_to_dict(self):
        self.assertDictEqual(self.course.to_dict(),{
            "course_id":"COR001",
            "course_name":"Systems Thinking and Design",
            "course_desc":"This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking",
            "course_status":"Active",
            "course_type":"Internal",
            "course_category":"Core"
        })

class TestStaff(unittest.TestCase):
    def setUp(self):
        self.staff1 = Staff(Staff_ID=130001,Staff_FName="John",Staff_LName="Sim",
        Dept="Chairman",Email="jack.sim@allinone.com.sg",Role=1)

    def tearDown(self):
        self.staff1 = None

    def test_to_dict(self):
        self.assertDictEqual(self.staff1.to_dict(),{
            "Staff_ID": 130001,
            "Staff_FName":"John",
            "Staff_LName": "Sim",
            "Dept": "Chairman",
            "Email": "jack.sim@allinone.com.sg",
            "Role": 1 
        })


class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.reg1 = Registration(reg_id=1,course_id="COR002",staff_id=130001,reg_status="Registered", completion_status="Completed")

    def tearDown(self):
        self.reg1 = None

    def test_to_dict(self):
        self.assertDictEqual(self.reg1.to_dict(),{
            "reg_id":1,
            "course_id":"COR002",
            "staff_id":130001,
            "reg_status":"Registered",
            "completion_status":"Completed"
        })

if __name__ == "__main__":
    unittest.main()
