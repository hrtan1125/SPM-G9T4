from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from flask_cors import CORS

# import json

app = Flask(__name__)
if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
                                            '@localhost:3306/testDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                            'pool_recycle': 280}
else:
     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

db = SQLAlchemy(app)

CORS(app)

class Roles(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50))
    deleted = db.Column(db.String(10))

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class Role_Skills(db.Model):
    __tablename__ = 'role_skills'
    row_id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, nullable=False)
    skill_code = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        """
            'to_dict' converts the object into a dictionary,
            in which the keys correspond to database columns
        """

        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def __init__(self, role_id, skill_code):
        self.role_id = role_id
        self.skill_code = skill_code


# admin create role
@app.route("/createrole", methods=['POST'])
def createRole():
    data = request.get_json()
    # print(data)
    # check if data format is correct
    if not "role_name" in data.keys() or not "skills" in data.keys():
        return jsonify(
            {
                "message": "Incorrect data format"
            }
        ), 400

    # check if the role already exists
    newRole = data["role_name"]
    checkRole = Roles.query.filter_by(role_name=newRole, deleted="no").first()
    if checkRole and checkRole.deleted!="yes":
            return jsonify(
                {
                    "message": "Role exists!"
                }
            ), 400

    role = Roles(**{"role_name":newRole,"deleted":"no"})

    try:
        db.session.add(role)
        db.session.flush()

        # add the role with skills
        # if not "skills" in data.keys():
        #     return jsonify({
        #         "message": "missing skills to be assigned."
        #     })
            
        skillsList = data['skills']
        assignSkill(skillsList,role.role_id)

        # commit everything together, to the role table and the skill table
        # this can be moved to the assignSkills function instead
        # db.session.commit()

        return jsonify(role.to_dict()), 200
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

# admin read all roles
@app.route("/viewroles")
def viewRoles():
    try: 
        data = Roles.query.filter_by(deleted="no").all()

        if data:
            return jsonify(
                {
                    "data": [role.to_dict() for role in data]
                }
            ), 200
        else:
            return jsonify(
                {
                    "message": "No role available."
                }
            ), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

    # admin read all roles
@app.route("/viewselectedrole")
def viewSelectedRole():
    try:
        # data = request.get_json()
        # role_id = data["role_id"]

        role_id = request.args["role_id"]
        selectedRole = Roles.query.filter_by(role_id=role_id).first()
        return jsonify(selectedRole.to_dict()), 201
    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        ),500

# admin update a role
@app.route("/updaterole", methods=['PUT'])
def updateRole():
    try:
        data = request.get_json()
        newRoleName = data['role_name']
        # check if new Role Name already exists
        checkRoleName = Roles.query.filter_by(role_name=newRoleName,deleted="no").first()
        
        if checkRoleName and checkRoleName.role_id!=int(data['role_id']):
            return jsonify(
                {
                    "message": "Role exists!"
                }
            ), 400

        # if not exists, update accordingly
        code = data['role_id']
        role = Roles.query.filter_by(role_id=code).first()

        if role:
            role.role_name = newRoleName
            db.session.commit()
            return jsonify(
                {
                    "message": "Role updated successfully."
                }
            ), 200
        else:
            return jsonify(
                {
                    "message": "Role not found!"
                }
            ), 400
    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        ), 500

# admin delete role (soft delete)
@app.route("/deleterole", methods=['PUT'])
def removeRole():
    try:
        data = request.get_json()
        role_id = data["role_id"]
        roleToDelete = Roles.query.filter_by(role_id=role_id).first()
        roleToDelete.deleted = "yes"

        db.session.commit()
        return jsonify({
            "message": "Role has been removed!"
        }), 200

    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        ), 500


#assign skills to role
@app.route("/assignSkills", methods=['POST'])
def assignSkill(skillslist=[], role_id=0):
    data = request.get_json()

    if data:
        if all(key in data.keys() for
                    key in ('role_id', 'skill_code')):
            print(data['role_id'])            
            role_id = data["role_id"]
            skillslist = data["skill_code"]

    for skill in skillslist:
        if (Role_Skills.query.filter_by(skill_code=skill, role_id=role_id).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "skill_code": skill,
                        "role_id": role_id
                    },
                    "message": "Skill is already assigned to role."
                }
            ), 400

        else:
            roleData = Role_Skills(**{"role_id": role_id,"skill_code":skill})

        try:
            db.session.add(roleData)
            db.session.commit()

        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "skill_code": skill,
                        "role_id": role_id
                    },
                    "message": "An error occurred when assigning the skill to role."
                }
            ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successful assignment of skill(s) to role"
        }
    ), 201




#Admin remove skills from role
@app.route("/removeSkills", methods=['DELETE'])
def removeSkill(skillslist=[], role_id=0):
    data = request.get_json()

    if data:
        if all(key in data.keys() for
                    key in ('role_id', 'skill_code')):
            print(data['role_id'])            
            role_id = data["role_id"]
            skillslist = data["skill_code"]

    if(skillslist == []):
        return jsonify(
        {
            "code": 201,
            "message": "No skill removed from role"
        }
    ), 201

    roleSkillsRecords = Role_Skills.query.filter_by(role_id=role_id).all()
    numOfRecords = 0
    for record in roleSkillsRecords:
        numOfRecords +=1

    if(numOfRecords == len(skillslist)):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "skill_code": skillslist,
                    "role_id": role_id
                },
                "message": "Skill(s) cannot be removed. A role must have at least one skill"
            }
        ), 400

    else:
        for skill in skillslist:            
            roleSkill = Role_Skills.query.filter_by(skill_code=skill, role_id=role_id).first()
            if (roleSkill):
                try:
                    db.session.delete(roleSkill)
                    db.session.commit()
                    numOfRecords -= 1

                except SQLAlchemyError as e:
                    print(e)
                    db.session.rollback()
                    return jsonify(
                        {
                            "code": 500,
                            "data": {
                                "skill_code": skill,
                                "role_id": role_id
                            },
                            "message": "An error occurred when removing skill from role."
                        }
                    ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successful removal of skill(s) from role"
        }
    ), 201
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)