import unittest
import flask_testing
import json
# from roles import app, db, Roles, Role_Skills
from skills import app, db, Skills

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

# view skills
class testSkills(TestApp):
    def test_view_skill(self):

        # from skills import Skills, db

        # request_body = {
        #     'skill_name':'Cost Management level 3'
        # }

        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")
        s3 = Skills(skill_code="COR111", skill_name="Software Project Management", deleted="yes")

        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        response = self.client.get("/view", content_type="application/json")

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
            "data": [
                {
                    "skill_code": "BF002",
                    "skill_name": "Cost Management level 3",
                    "deleted": "no"
                    
                },{
                    "skill_code": "BOM001",
                    "skill_name": "Strategy Development level 3",
                    "deleted": "no"
                    
                }
            ]
        })
        
    class testViewSelectedSkill(TestApp):
        def test_view_selected_skill(self):

            s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
            s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")
            s3 = Skills(skill_code="COR111", skill_name="Software Project Management", deleted="yes")

            db.session.add(s1)
            db.session.add(s2)
            db.session.add(s3)
            db.session.commit()

            response = self.client.get("/viewselectedskill", content_type="application/json", header="skill_code=BF002")

            self.assertEqual(response.status_code,201)
            self.assertDictEqual(response.json, {
                "skill_code": "BF002",
                "skill_name": "Cost Management level 3",
                "deleted": "no"
            })



    class testEditSkill(TestApp):
        def test_edit_skill_with_existing_skill_code_and_name(self):
            s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
            s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")
            s3 = Skills(skill_code="COR111", skill_name="Software Project Management", deleted="yes")

            db.session.add(s1)
            db.session.add(s2)
            db.session.add(s3)
            db.session.commit()

            request_body = {
                'skill_code':'COR111',
                'skill_name':'Software Project Management'
            }
            
            response = self.client.put("/update",
                                        data=json.dumps(request_body),
                                        content_type='application/json')
            
            self.assertEqual(response.status_code,400)
            self.assertDictEqual(response.json,{
                "message": "Skill already exists!"
            })
    
        def test_edit_skill_with_non_existing_skill_code_and_name(self):
            s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
            s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")
            s3 = Skills(skill_code="COR111", skill_name="Software Project Management", deleted="yes")

            db.session.add(s1)
            db.session.add(s2)
            db.session.add(s3)
            db.session.commit()

            request_body = {
                'skill_code':'COR000',
                'skill_name':'Software Project Management'
            }
            
            response = self.client.put("/update",
                                        data=json.dumps(request_body),
                                        content_type='application/json')
            
            self.assertEqual(response.status_code,200)
            self.assertDictEqual(response.json,{
                "message": "Skill code not found!"
            })
            


if __name__ == '__main__':
    unittest.main()
