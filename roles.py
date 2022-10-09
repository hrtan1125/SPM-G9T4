from crypt import methods
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/projectDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

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
    rowid = db.Column(db.Integer, primary_key=True)
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
@app.route("/create", methods=['POST'])
def createRole():
    data = request.get_json()
    
    # check if data format is correct
    if not "role_name" in data.keys():
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

    # if not all(key in data.keys() for
    #            key in ('role_name', 'deleted')):
    #     return jsonify(
    #         {
    #             "message": "Incorrect data format."
    #         }
    #     ), 404
    role = Roles(**{"role_name":newRole,"deleted":"no"})

    try:
        db.session.add(role)
        db.session.flush()

        # add the role with skills
        if not "skills" in data.keys():
            return jsonify({
                "message": "missing skills to be assigned."
            })
            
        skillsList = data['skills']
        assignSkill(skillsList,role.role_id)

        # commit everything together, to the role table and the skill table
        # this can be moved to the assignSkills function instead
        db.session.commit()

        return jsonify(role.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 400

# admin read all roles
@app.route("/view")
def viewRoles():
    data = Roles.query.all()
    return jsonify(
        {
            "data": [role.to_dict() for role in data]
        }
    ), 200

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
        )

# admin update a role
@app.route("/update", methods=['PUT'])
def updateRole():
    try:
        data = request.get_json()
        newRoleName = data['role_name']

        # check if new Role Name already exists
        checkRoleName = Roles.query.filter_by(role_name=newRoleName,deleted="no").first()

        if checkRoleName:
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
        ), 400

# admin delete role (soft delete)
@app.route("/delete", methods=['PUT'])
def removeRole():
    try:
        data = request.get_json()
        role_id = data["role_id"]
        roleToDelete = Roles.query.filter_by(role_id=role_id).first()
        roleToDelete.deleted = "yes"

        db.session.commit()
        return jsonify({
            "message": "Role has been removed!"
        })

    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        )

#to be removed from here
@app.route("/viewRoleSkills", methods=['GET'])
def viewRoleSkills():
    search_skill = request.args.get('role_id')
    if search_skill:
        skills = Role_Skills.query.filter_by(role_id=search_skill).all()
        return jsonify({
            "data": [skill.skill_code for skill in skills]
        })
    else:
        return jsonify({
            "message": "Missing Input."
        }), 400


# admin assign skills, still need changes
# directly call from http
@app.route("/assignSkills", methods=['POST'])
def assignSkill(skillslist, role_id):
    for skill in skillslist:
        roleData = Role_Skills(**{"role_id": role_id,"skill_code":skill})
        db.session.add(roleData)
    
    # alternatively, do db.session.commit() here
    return

### skill assign to role start here###
@app.route("/role_skill/all", methods=['GET'])
def get_all():
    all_role_skill_list = Role_Skills.query.all()
    if len(all_role_skill_list):
        return jsonify(
            {
                "code":200,
                "data": {
                    "role": [role.to_dict() for role in all_role_skill_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404, 
            "message": "No entries found"
        }
    ), 404


@app.route("/role_skill", methods=['POST'])
def assign_skills_to_role():
    data = request.get_json()  # py obj
    role_id = data['role_id']
    skills = data['skill_code']

    for skill in skills:
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
            role_skill = Role_Skills(role_id, skill)

        try:
            db.session.add(role_skill)

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

    db.session.commit()

    return jsonify(
        {
            "code": 201,
            "message": "Successful assignment of skill(s) to role"
        }
    ), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)