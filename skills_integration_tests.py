import unittest
import flask_testing
import json
# from roles import app, db, Roles, Role_Skills
from skills import app, db, Skills, Skills_acquired, Course_skills

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

# create skills 
class testCreateSkill(TestApp): 
    def test_create_skill(self):

        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_name':'Chief Technology Officer',
            'skill_code':'COR002'
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertDictEqual(response.json, {
            "data": [{
                "skill created": {
                    "deleted": "no",
                    "skill_code": "COR002",
                    "skill_name": "Chief Technology Officer"
                    }
                },
                {
                "message": "Skill created successfully."
                }
            ]
        })

    def test_create_with_existing_skill_code_and_name(self):

        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_name':'Cost Management level 3',
            'skill_code':'BF002'
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Skill code and name already exist!"
        })
    
    def test_create_with_existing_skill_code(self):

        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_name':'Cost Management level 4',
            'skill_code':'BF002'
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Skill code already exist!"
        })
    
    def test_create_with_existing_skill_code(self):

        s1 = Skills(skill_code="BF003", skill_name="Cost Management level 3", deleted="no")
        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_name':'Cost Management level 3',
            'skill_code':'BF002'
        }

        response = self.client.post("/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "Skill name already exist!"
        })
    


# view skills
class testSkills(TestApp):
    def test_view_skill(self):

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

        response = self.client.get("/viewselectedskill?skill_code=BF002", 
                                    content_type="application/json")

        self.assertEqual(response.status_code,201)
        self.assertDictEqual(response.json, {
            "skill_code": "BF002",
            "skill_name": "Cost Management level 3",
            "deleted": "no"
        })


class testEditSkill(TestApp):
    def test_edit_skill(self):
        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")
        s3 = Skills(skill_code="COR111", skill_name="Software Project Management", deleted="yes")

        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        request_body = {
            'skill_code':'BF002',
            'skill_name':'Cost Management level 4'
        }
            
        response = self.client.put("/update",
                                    data=json.dumps(request_body),
                                    content_type='application/json')
            
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.json,{
            "message": "Skill name updated successfully."
        })    
            
    def test_edit_skill_with_existing_skill_code_and_name(self):
        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")

        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        request_body = {
            'skill_code':'BOM001',
            'skill_name':'Strategy Development level 3'
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
            
        self.assertEqual(response.status_code,404)
        self.assertDictEqual(response.json,{
            "message": "Skill code not found!"
        })

#delete role
class testDeleteSkill(TestApp):
    def test_delete_existing_skill(self):
        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")

        db.session.add(s1)
        db.session.commit()

        request_body = {
            'skill_code':'BF002'
        }

        response = self.client.put("/delete",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
            "message": "Skill has been removed!"
        })
    
    def test_delete_non_existing_skill(self):
        s1 = Skills(skill_code="BF002", skill_name="Cost Management level 3", deleted="no")
        s2 = Skills(skill_code="BOM001", skill_name="Strategy Development level 3", deleted="no")
        s3 = Skills(skill_code="COR111", skill_name="Software Project Management", deleted="yes")

        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        request_body = {
            'skill_code':'COR111'
        }

        response = self.client.put("/delete",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json,{
            "message": "Skill no longer available."
        })

class testViewLearnerSkills(TestApp):
    def test_view_learner_skills(self):
        skA1 = Skills_acquired(staff_id="140115",skill_code="GM003")
        skA2 = Skills_acquired(staff_id="140115",skill_code="GM004")
        s1 = Skills(skill_code="GM003", skill_name="French Cooking",deleted="no")
        s2 = Skills(skill_code="GM004", skill_name="Italian Cooking",deleted="no")
        db.session.add(skA1)
        db.session.add(skA2)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        
        response = self.client.get("/viewLearnersSkills?staff_id=140115",
                                    content_type='application/json')
        
        self.assertEqual(response.status_code,200)
        self.assertDictEqual(response.json,{
            "data": [
                {
                    "GM003":"French Cooking"
                },
                {
                    "GM004":"Italian Cooking"
                }]
        })
    def test_view_learner_skills_with_no_staffid(self):
        skA1 = Skills_acquired(staff_id="140115",skill_code="GM003")
        s1 = Skills(skill_code="GM003", skill_name="French Cooking",deleted="no")
        db.session.add(skA1)
        db.session.add(s1)
        db.session.commit()
        
        response = self.client.get("/viewLearnersSkills",
                                    content_type='application/json')
        
        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json,{
            "message": "No staffID."
        })
# class test_View_skills_to_add(TestApp):
#     def test_view_skills_to_add(self):
#         s1 = Skills(skill_code="GM003", skill_name="Change Management level 3", deleted="no")
#         c1 = Courses(course_id="COR002", course_name="Lean Six Sigma Green Belt Certification", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
#         cs1 = Course_skills(course_id="COR002", skill_code="GM003")
#         db.session.add(s1)
#         db.session.add(c1)
#         db.session.add(cs1)
#         db.session.commit()

        
#         response = self.client.get("/view_skills_to_add/COR002",
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code,200)
#         self.assertDictEqual(response.json,{
#             "skills": [
#                 "GM003"
#             ]
#         })

#     def test_view_skills_to_add_not_assigned(self):
#         s1 = Skills(skill_code="GM003", skill_name="Change Management level 3", deleted="no")
#         c1 = Courses(course_id="COR001", course_name="Systems Thinking and Design", course_desc="Course description here", course_status="Active", course_type="Internal", course_category="Core")
#         cs1 = Course_skills(course_id="COR002", skill_code="GM003")
#         db.session.add(s1)
#         db.session.add(c1)
#         db.session.add(cs1)
#         db.session.commit()

        
#         response = self.client.get("/view_skills_to_add/COR001",
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code,200)
#         self.assertDictEqual(response.json,{
#             "message": "no skills assigned to the course yet."
#         })
    
class Test_skill_assigns_course(TestApp):
    # def test_skill_assigns_course(self):
    #     cs1 = Course_skills(course_id="COR002", skill_code="GM004")
    #     db.session.add(cs1)
    #     db.session.commit()

    #     request_body = {
    #         "course_id": "COR001" ,
    #         "skills": "GM003"
    #     }
    #     response = self.client.post("/skill_assigns_course",
    #                                 data=json.dumps(request_body),
    #                                 content_type='application/json')

    #     self.assertEqual(response.status_code,200)
    #     self.assertDictEqual(response.json, {
    #         "message": "Course and Skills successfully updated"
    #     })
    def test_skill_assigns_course_assigned(self):
        cs1 = Course_skills(course_id="COR001", skill_code="GM003")
        db.session.add(cs1)
        db.session.commit()
        
        request_body = {
            
            "course_id": "COR001" ,
            "skills": "GM003"
            
        }

        response = self.client.post("/skill_assigns_course",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertDictEqual(response.json, {
            "message": "skill for this course already exist"
        })

# class Test_viewSkillsByRole(TestApp):
#     def test_viewSkillsByRole(self):
#         s1 = Skills(skill_code="GM003", skill_name="Change Management level 3", deleted="no")
#         db.session.add(s1)
#         db.session.commit()

#         request_body = {
#             'RoleSkills': {"1":["GM003"]}
#         }

#         response = self.client.post("/viewRoleSkills",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code,200)
#         self.assertDictEqual(response.json, {
#             "message": "Course and Skills successfully updated"
#         })
#     def test_viewSkillsByRole_missing_input(self):
#         s1 = Skills(skill_code="GM003", skill_name="Change Management level 3", deleted="no")
#         db.session.add(s1)
#         db.session.commit()
        
#         request_body = {
#             'RoleSkills': {"1":["GM003"]}
#         }
        
#         response = self.client.post("/viewRoleSkills",
#                                     data=json.dumps(request_body),
#                                     content_type='application/json')

#         self.assertEqual(response.status_code,400)
#         self.assertDictEqual(response.json, {
#             "message": "skill for this course already exist"
#         })
# class test_viewRoleSkills(TestApp):
#     def test_viewRoleSkills(self):
#         rs1 = Role_Skills(role_id=1, skill_code="GM003")
#         s1 =  Skills(skill_code="GM003", skill_name="Change Management level 3",deleted="no")
#         s1 =  Skills(skill_code="PF003", skill_name="Financial Analysis level 3",deleted="no")
#         db.session.add(rs1)
#         db.session.add(s1)
#         db.session.add(s1)
#         db.session.commit()

#         response = self.client.get("/viewRoleSkills?role_id=1",
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code,201)
#         self.assertDictEqual(response.json,{
#             "data": {
#                 "GM003": {
#                     "deleted": "no",
#                     "skill_code": "GM003",
#                     "skill_name": "Change Management level 3"
#                 },
#                 "PF003": {
#                     "deleted": "no",
#                     "skill_code": "PF003",
#                     "skill_name": "Financial Analysis level 3"
#                 }
#             }
#         })
#     def test_viewRoleSkills_missing_input(self):
#         rs1 = Role_Skills(role_id=1, skill_code="GM003")
#         s1 =  Skills(skill_code="GM003", skill_name="Change Management level 3",deleted="no")
#         s1 =  Skills(skill_code="PF003", skill_name="Financial Analysis level 3",deleted="no")
#         db.session.add(rs1)
#         db.session.add(s1)
#         db.session.add(s1)
#         db.session.commit()

#         response = self.client.get("/viewRoleSkills",
#                                     content_type='application/json')
        
#         self.assertEqual(response.status_code,400)
#         self.assertDictEqual(response.json,{
#             "message": "Missing Input."
#         })

if __name__ == '__main__':
    unittest.main()
