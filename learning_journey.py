from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import null
from roles import Role_Skills
from skills import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/projectDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Learning_Journey(db.Model):
    __tablename__ = 'learning_journey'

    lj_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    role_id = db.Column(db.Integer)
    staff_id = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'learning_journey'
    }

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

class Learning_Journey_Courses(db.Model):
    __tablename__ = 'learning_journey_courses'

    lj_id = db.Column(db.Integer)
    skill_code = db.Column(db.String(20))
    course_id = db.Column(db.String(20))
    row_id = db.Column(db.Integer, primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'learning_journey_courses'
    }

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

class Courses(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.String(20), primary_key=True)
    course_name = db.Column(db.String(50))
    course_desc = db.Column(db.String(255))
    course_status = db.Column(db.String(15))
    course_type = db.Column(db.String(10))
    course_category = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'courses'
    }

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

# after user select a role, show them the skills available
@app.route("/viewRoleSkills", methods=['GET'])
def viewRoleSkills():
    search_skill = request.args.get('role_id')
    try:
        if search_skill:
            RoleSkills = Role_Skills.query.filter_by(role_id=search_skill).all()
            skills = [skill.skill_code for skill in RoleSkills]
            skillslist = Skills.query.filter(Skills.skill_code.in_(skills)).all()

            return jsonify({
                "data": [skill.to_dict() for skill in skillslist]
            }), 200
        else:
            return jsonify({
                "message": "Missing Input."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

#and then show then the courses available based on the selected skill
@app.route("/viewCourses", methods=['GET'])
def viewCourses():
    skill =  request.args.get('skill_code')
    try:
        if skill:
            CoursesList = Course_skills.query.filter_by(skill_code=skill).all()
            
            CoursesId = [course.course_id for course in CoursesList]
            print(CoursesId) #to be removed
            courses =  Courses.query.filter(Courses.course_id.in_(CoursesId)).all()
            return jsonify(
                {
                    "data": [course.to_dict() for course in courses]
                }
            ), 200
        else:
            return jsonify({
                "message": "Missing Input."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500   

@app.route("/createlearningjourney", methods=['POST'])
def create_learningjourney():
    data = request.get_json()

    ##checking for correct data type
    if not all(key in data.keys() for
               key in ('title',
                       'role_id', 
                       'staff_id', 'courses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
    title = data["title"]
    role_id = data["role_id"]
    staff_id = data["staff_id"]
    courses_list = data["courses"]
    # {skill_code1:[courses], skill_code2:[courses]}

    learning_journey = Learning_Journey(**{"title": title,"role_id":role_id, "staff_id":staff_id})
    
    try:
        db.session.add(learning_journey)
        db.session.flush()

        #get learning_journey id
        id = learning_journey.lj_id

        #call function to add courses to learning journey
        add_learningjourneycourses(id,courses_list)
        # db.session.commit() <-- this one dont need, cuz you will commit everything in one time at line 142
        return jsonify(learning_journey.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

#to handle a list of courses
# parameters: lj_id, courses in this format {skill_code1:[courses], skill_code2:[courses],...}
@app.route("/addlearningjourneycourses", methods=['POST'])
def add_learningjourneycourses(lj_id=0,courses=null):
    data = request.get_json()
    if data:
        if all(key in data.keys() for
                    key in ('lj_id','courses')):
            print(data['lj_id'])
            courses = data["courses"]
            lj_id = data["lj_id"]

    ##checking for correct data type
    ## can remove this I think
    # if not all(key in data.keys() for
    #            key in ('lj_id',
    #                     'skill_code',
    #                     'course_id')):
    #     return jsonify({
    #         "message": "Incorrect JSON object provided."
    #     }), 500

    ##check if learning journey already has that course (No need thanks to function in later sprint)
    # lj_id = data["lj_id"]
    # skill_code = data["skill_code"]
    # course_id = data["course_id"]

    # row_id = 11 <-- no need, cuz db will do auto increment
    # need for loop I guess cuz is list of courses
    # something like this bah but i haven't test
    

    # learning_journey_courses = Learning_Journey_Courses(**{"lj_id": lj_id,"skill_code":skill_code, "course_id":course_id})
    # checkCourse = Learning_Journey_Courses.query.filter_by(lj_id = lj_id, course_id = course_id).first()
    # if checkRole and checkRole.deleted!="yes":
    #         return jsonify(
    #             {
    #                 "message": "This course is already in the selected learning journey!"
    #             }
    #         ), 400
    try:
        # for loop move here, line 139 can remove
        # keep line 142 outside the whole for loop
        # move it to inside the 'try'
        for skill in courses.keys():
            for course in courses[skill]:
                learning_journey_course = Learning_Journey_Courses(**{"lj_id": lj_id,"skill_code":skill, "course_id":course})
                db.session.add(learning_journey_course)
        # db.session.add(learning_journey_courses)
        # db.session.flush()
        db.session.commit()
        # return jsonify(learning_journey_courses.to_dict()), 201
        return jsonify({
            "message": "Learning Journey successfully created!"
        })
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
