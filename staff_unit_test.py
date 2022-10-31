import unittest
from learning_journey import Staff


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
 
if __name__ == "__main__":
    unittest.main()