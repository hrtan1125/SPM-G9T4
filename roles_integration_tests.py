import unittest
import flask_testing
import json
from roles import app, db, Roles, Role_Skills

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

#create role
class testCreateRole(TestApp):
    def test_create_role(self):
        request_body = {
            'role_name':'Chief Technology Officer',
            'skills':['COR002','PD012']
        }

        response = self.client.post("/createrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertDictEqual(response.json, {
            'role_id': 1,
            'role_name': 'Chief Technology Officer',
            'deleted': 'no'
        })
    
    def test_create_role_with_exist_role_name(self):

        #create the first role
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")
        db.session.add(r1)
        db.session.commit()

        #create the same role again
        request_body = {
            'role_name':'Chief Technology Officer',
            'skills':['COR002','PD012']
        }

        response = self.client.post("/createrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertDictEqual(response.json, {
            "message": "Role exists!"
        })

    def test_create_role_with_deleted_role_name(self):
        #create the first role with deleted = yes
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="yes")
        db.session.add(r1)
        db.session.commit()

        #create the same role again
        request_body = {
            'role_name':'Chief Technology Officer',
            'skills':['COR002','PD012']
        }

        response = self.client.post("/createrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
            'role_id': 2,
            'role_name': 'Chief Technology Officer',
            'deleted': 'no'
        })

#view roles
class testViewRoles(TestApp):
    def test_view_role(self):
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")
        r2 = Roles(role_id=2, role_name="Supervisor", deleted="no")
        r3 = Roles(role_id=3, role_name="Project Design Executive", deleted="yes")

        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()

        response = self.client.get("/viewroles", content_type="application/json")

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json, {
            "data": [
                {
                    "role_id":1,
                    "role_name": "Chief Technology Officer",
                    "deleted": "no"
                },
                {
                    "role_id":2,
                    "role_name": "Supervisor",
                    "deleted": "no"
                }
            ]
        })

    def test_view_roles_no_available(self):
        response = self.client.get("/viewroles", content_type="application/json")

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message":"No role available."
        })

#update role
class testUpdateRole(TestApp):
    def test_update_role(self):
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")
        db.session.add(r1)
        db.session.commit()

        request_body = {
            'role_id':'1',
            'role_name':'Chief Executive Officer'
        }

        response = self.client.put("/updaterole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
            "message": "Role updated successfully."
        })

    def test_update_role_with_existing_role_name(self):
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")
        r2 = Roles(role_id=2, role_name="Chief Executive Officer", deleted="no")

        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()

        request_body = {
            'role_id':'1',
            'role_name':'Chief Executive Officer'
        }

        response = self.client.put("/updaterole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json,{
            "message": "Role exists!"
        })

    def test_update_role_with_invalid_role_id(self):
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")

        db.session.add(r1)
        db.session.commit()

        request_body = {
            'role_id':'2',
            'role_name':'Chief Executive Officer'
        }

        response = self.client.put("/updaterole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json,{
            "message": "Role not found!"
        })

#delete role
class testDeleteRole(TestApp):
    def test_delete_role(self):
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")

        db.session.add(r1)
        db.session.commit()

        request_body = {
            'role_id':'1'
        }

        response = self.client.put("/deleterole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
            "message": "Role has been removed!"
        })
class test_viewSelectedRole(TestApp):
    def test_viewSelectedRole(self):
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")
        db.session.add(r1)
        db.session.commit()

        
        response = self.client.get("/viewselectedrole?role_id=1",
                                    content_type='application/json')
        
        self.assertEqual(response.status_code,201)
        self.assertDictEqual(response.json,{
            "deleted": "no",
            "role_id": 1,
            "role_name": "Chief Technology Officer"
        })
class Test_assignSkill(TestApp):
    def test_assignSkill(self):

        request_body = {
            "role_id": 1 ,
            "skills": ["GM003"]
        }
        response = self.client.post("/assignSkills",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,201)
        self.assertDictEqual(response.json, {
            "code": 201,
            "message": "Successful assignment of skill(s) to role"
        })

    # def test_skill_assigns_course_assigned(self):
    #     rs1 = Role_Skills(role_id=1, skill_code="GM003")
    #     db.session.add(rs1)
    #     db.session.commit()
        
    #     request_body = {
    #         "role_id": 1 ,
    #         "skills": ["GM003"]
    #     }

    #     response = self.client.post("/skill_assigns_course",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')

    #     self.assertEqual(response.status_code,400)
    #     self.assertDictEqual(response.json, {
    #                 "code": 400,
    #                 "data": {
    #                     "skill_code": "GM003",
    #                     "role_id": 1
    #                 },
    #                 "message": "Skill is already assigned to role."
    #             }
    #         )
if __name__ == '__main__':
    unittest.main()

