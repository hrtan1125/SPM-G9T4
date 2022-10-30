import unittest
from learning_journey import Learning_Journey

class TestLearningJourney(unittest.TestCase):
    def test_to_dict(self):
        p1 = Learning_Journey(title='Test Title', role_id='3', staff_id='150166')
        self.assertEqual(p1.to_dict(), {
            'lj_id': None,
            'title': 'Test Title',
            'role_id': '3',
            'staff_id': '150166'}
        )

class TestLearningJourneyProgress(unittest.TestCase):
    def test_progress(self):
        courses_and_statuses = [['Completed', 'COR002', 'Lean Six Sigma Green Belt Certification'], ['', 'FIN001', 'Data Collection and Analysis']]
        progress = Learning_Journey.calculate_progress(courses_and_statuses)
        self.assertEqual(progress, 
            50.0)
    def test_progress_zero(self):
        courses_and_statuses = [["Waitlist", "COR002", "Lean Six Sigma Green Belt Certification"]]
        progress = Learning_Journey.calculate_progress(courses_and_statuses)
        self.assertEqual(progress, 
            0.0)
    def test_progress_empty(self):
        with self.assertRaises(Exception):
            courses_and_statuses = []
            progress = Learning_Journey.calculate_progress(courses_and_statuses)
    
if __name__ == "__main__":
    unittest.main()
