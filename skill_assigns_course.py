import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/projectdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size':100, 'pool_recycle': 28}

db = SQLAlchemy(app)
CORS(app)

class Course_skills(db.Model):
    __tablename__ = 'course_skills'
    row_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20))
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

    def __init__(self, course_id, skill_code):
        self.course_id = course_id
        self.skill_code = skill_code


@app.route("/skill_assigns_course/all", methods=['GET'])
def get_all():
    all_list = Course_skills.query.all()
    if len(all_list):
        return jsonify(
            {
                "code":200,
                "data": {
                    "course": [course.to_dict() for course in all_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404, 
            "message": "There is no entry"
        }
    ), 404

@app.route("/skill_assigns_course", methods=['POST'])
def skill_assigns_course():

    # assumption here is that the course name is given
    # the skills are given in the body 
    #   {
    #       "course_id": "IS226", 
    #       "skill_code": ["CS04", "DA04", "CM04"] 
    #   }

    #check if exists
    data = request.get_json() #py obj
    course_id = data['course_id']
    # if (Course_skills.query.filter_by(course_id=course_id).first()):
    #     return jsonify(
    #         {
    #             "code": 400, 
    #             "data": {
    #                 "course_id": course_id
    #             }, 
    #             "message": "Course already exist"
    #         }
    #     ), 400

    
    skill_code = data['skill_code'] #list

    try:
        
        for skill in skill_code:
            #check if the combination of course and skill exists
            if (Course_skills.query.filter_by(course_id=course_id, skill_code=skill).first()):
                return jsonify(
                    {
                        "code": 400,
                        "message": "skill for this course already exist"
                    }
                )
            course_skill = Course_skills(course_id, skill)
            db.session.add(course_skill)
        db.session.commit()
            

    except SQLAlchemyError as e:
        print(e)

    
    return jsonify(
            {
                "code": 201,
                "message": "Course and Skills successfully updated"
            }
        )
        


if __name__ == '__main__':
    app.run(port=5000, debug=True)
