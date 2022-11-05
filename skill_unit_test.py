import unittest
from skills import Skills, Course_skills, Skills_acquired

class TestSkills(unittest.TestCase):
    def setUp(self):
        self.s1 = Skills(skill_code="COR111",skill_name="Software Project Management",deleted="no")

    def tearDown(self):
        self.s1 = None
    
    def test_skills_to_dict(self):
        self.assertDictEqual(self.s1.to_dict(),{
            "skill_code":"COR111",
            "skill_name":"Software Project Management",
            "deleted":"no"
        })

class TestCourseSkills(unittest.TestCase):
    def setUp(self):
        self.cs1 = Course_skills(course_id="COR002",skill_code="GM003")

    def tearDown(self):
        self.cs1 = None

    def test_course_skills_to_dict(self):
        self.assertDictEqual(self.cs1.to_dict(),{
            "row_id":None,
            "course_id":"COR002",
            "skill_code":"GM003"
        })

class TestSkillsAcquired(unittest.TestCase):
    def setUp(self):
        self.sa1 = Skills_acquired(staff_id="140115",skill_code="GM003")

    def tearDown(self):
        self.sa1 = None

    def test_skills_acquired_to_dict(self):
        self.assertDictEqual(self.sa1.to_dict(),{
            "row_id":None,
            "staff_id":"140115",
            "skill_code":"GM003"
        })
 
if __name__ == "__main__":
    unittest.main()