from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from skills import Skills

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
    role_id = db.Column(db.Integer)
    skill_code = db.Column(db.String(20))

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
        # this can be move to be done in the assignSkills function instead as well
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
    # multi-select delete
    try:
        data = request.get_json()
        roles = data["roles"]
        RolesToDelete = Roles.query.filter(Roles.role_id.in_(roles))

        for role in RolesToDelete:
            role.deleted = "yes"

        db.session.commit()
        return jsonify({
            "message": "Roles have been removed!"
        })

    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        )

# admin assign skills, still need changes
# directly call from http
@app.route("/assignSkills", methods=['POST'])
def assignSkill(skillslist, role_id):
    for skill in skillslist:
        roleData = Role_Skills(**{"role_id": role_id,"skill_code":skill})
        db.session.add(roleData)
    
    # alternatively, do db.session.commit() here
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)