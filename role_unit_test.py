import unittest
from roles import Roles

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


if __name__ == "__main__":
    unittest.main()
