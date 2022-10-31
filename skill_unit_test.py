import unittest
from skills import Course_skills


class TestCourse_skills(unittest.TestCase):
    def setUp(self):
        self.cs1 = Course_skills(course_id="COR002",skill_code="GM003")

    def tearDown(self):
        self.cs1 = None

    def test_to_dict(self):
        self.assertDictEqual(self.cs1.to_dict(),{
            "row_id":None,
            "course_id":"COR002",
            "skill_code":"GM003"
        })
 
if __name__ == "__main__":
    unittest.main()