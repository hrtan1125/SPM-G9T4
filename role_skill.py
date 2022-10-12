# assign skills to role
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
# import json
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/projectdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)


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

    # def json(self):
    #     return {"role_id": self.role_id, "skill_code": self.skill_code}

# [very important] for all backend coder:
# return your data in this way
# jsonify({“data”: xxx}), 200 [successful]
# jsonify({“message”: xxx}),400 [not successful]

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
    app.run(port=5000, debug=True)