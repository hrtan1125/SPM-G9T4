import unittest
from roles import Role_Skills, Roles

class TestRoles(unittest.TestCase):
    def setUp(self):
        self.r1 = Roles(role_id=1, role_name="Supervisor", deleted="no")
        self.r2 = Roles(role_id=2, role_name="President", deleted="no")

    def tearDown(self):
        self.r1 = None
        self.r2 = None

    def test_to_dict(self):
        result = self.r2.to_dict()
        self.assertDictEqual(result, {"role_id":2, "role_name":"President", "deleted": "no"})

class TestRoleSkills(unittest.TestCase):
    def setUp(self):
        self.rs1 = Role_Skills(row_id=1,role_id=1,skill_code="COR002")

    def tearDown(self):
        self.rs1 = None

    def test_to_dict(self):
        result = self.rs1.to_dict()
        self.assertDictEqual(result, {"row_id":1, "role_id":1, "skill_code": "COR002"})

if __name__ == "__main__":
    unittest.main()
