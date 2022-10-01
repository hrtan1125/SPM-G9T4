from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
                                        '@localhost:3306/projectDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Skills(db.Model):
    __tablename__ = 'skills'

    skill_code = db.Column(db.String(20) , primary_key=True)
    skill_name = db.Column(db.String(100))
    deleted = db.Column(db.String(10))

    __mapper_args__ = {
        'polymorphic_identity': 'skills'
    }

    def to_dict(self):

        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

db.create_all()

@app.route("/create", methods=['POST'])  #create skill
def create_skill():
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('skill_code', "skill_name")):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
    new_skill = data["skill_name"]
    check_skill = Skills.query.filter_by(skill_name=new_skill, deleted="no").first()
    if check_skill:
        return jsonify(
                {
                    "message": "Skill already exist!"
                }), 400
    skill = Skills(**data)
    try:
        db.session.add(skill)
        db.session.commit()
        return jsonify(skill.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

@app.route("/view") #get skills 
def skills():
    search_skill = request.args.get('skill_name')
    if search_skill:
        skill_list = Skills.query.filter(Skills.skill_name.contains(search_skill))
    else:
        skill_list = Skills.query.filter_by(deleted = "no").all()
    return jsonify(
        {
            "data": [skill.to_dict() for skill in skill_list]
        }
    ), 200


@app.route("/update", methods=['PUT']) #edit
def edit_skill():
    data = request.get_json()
    skill_code = data["skill_code"]
    skill_name = data["skill_name"]
    check_skill_name = Skills.query.filter_by(skill_name=skill_name,deleted="no").first()
    if check_skill_name:
        return jsonify(
                {
                    "message": "Skill already exists!"
                }), 400
    skill = Skills.query.filter_by(skill_code=skill_code).first()
    if not skill:
        return jsonify(
            {
                "message": "Skill code not found!"
            }
            ), 404
    
    else:
        skill.skill_name = skill_name
    try: 
        db.session.commit()
        return jsonify({"message": "Skill name updated successfully."}), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

@app.route("/delete", methods=['PUT'])
def delete_skill():  #delete skill
    data = request.get_json()
    for todelete in data:
        skill_code = todelete["skill_code"]
        deleteskill = Skills.query.filter_by(skill_code = skill_code).first()
        deleteskill.deleted = "yes"
            
    try: 
        db.session.commit()
        jsonify({"Message": "Skills deleted successfully"}), 201
    except Exception:
        return jsonify({
            "message": "Unable to delete skill."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
