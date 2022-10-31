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

class testCreateRole(TestApp):
    def test_create_role(self):
        print("testing create new role")
        request_body = {
            'role_name':'Chief Technology Officer',
            'skills':['COR002','PD012']
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertDictEqual(response.json, {
            'role_id': 1,
            'role_name': 'Chief Technology Officer',
            'deleted': 'no'
        })
    
    def test_create_role_with_exist_role_name(self):
        print("testing create new role with existed name")

        #create the first role
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="no")
        db.session.add(r1)
        db.session.commit()

        #create the same role again
        request_body = {
            'role_name':'Chief Technology Officer',
            'skills':['COR002','PD012']
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertDictEqual(response.json, {
            "message": "Role exists!"
        })

    def test_create_role_with_deleted_role_name(self):
        print("testing create new role with existed name")

        #create the first role
        r1 = Roles(role_id=1, role_name="Chief Technology Officer", deleted="yes")
        db.session.add(r1)
        db.session.commit()

        #create the same role again
        request_body = {
            'role_name':'Chief Technology Officer',
            'skills':['COR002','PD012']
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertDictEqual(response.json, {
            'role_id': 2,
            'role_name': 'Chief Technology Officer',
            'deleted': 'no'
        })

if __name__ == '__main__':
    unittest.main()

