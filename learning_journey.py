from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import null
from roles import Role_Skills
from skills import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
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

# view courses
@app.route("/viewAllCourses", methods=['GET'])
def viewAllCourses():
    try:
        courses = Courses.query.filter_by(course_status="Active").all()
        if courses:
            return jsonify({
                "data": [course.to_dict() for course in courses]
            }), 200
        else:
            return jsonify({
                "message": "No courses available."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
        }), 500


# after user select a role, show them the skills available
@app.route("/viewRoleSkills", methods=['GET'])
def viewRoleSkills():
    search_skill = request.args.get('role_id')
    try:
        if search_skill:
            RoleSkills = Role_Skills.query.filter_by(role_id=search_skill).all()
            skills = [skill.skill_code for skill in RoleSkills]
            skillslist = Skills.query.filter(Skills.skill_code.in_(skills),Skills.deleted=="no").all()

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
            
            courses =  Courses.query.filter(Courses.course_id.in_(CoursesId),Courses.course_status=="Active").all()
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
def create_learning_journey():
    data = request.get_json()

    ##checking for correct data type
    if not all(key in data.keys() for
               key in ('title',
                       'role_id', 
                       'staff_id', 'courses')):
        return jsonify({
            "message": "Incorrect Data Formet."
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
        add_learning_journey_courses(id,courses_list)

        return jsonify(learning_journey.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

#to handle a list of courses
# parameters: lj_id, courses in this format {skill_code1:[courses], skill_code2:[courses],...}
@app.route("/addlearningjourneycourses", methods=['POST'])
def add_learning_journey_courses(lj_id=0,courses=[]):
    data = request.get_json()
    if data:
        if all(key in data.keys() for
                    key in ('lj_id','courses')):
            print(data['lj_id'])
            courses = data["courses"]
            lj_id = data["lj_id"]

    try:
        for skill in courses.keys():
            for course in courses[skill]:
                learning_journey_course = Learning_Journey_Courses(**{"lj_id": lj_id,"skill_code":skill, "course_id":course})
                db.session.add(learning_journey_course)
        db.session.commit()
        
        return jsonify({
            "message": "Courses successfully added!"
        })
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

@app.route("/removecourses", methods=['DELETE'])
def removeCourses():
    data = request.get_json()
    id = data['lj_id']
    course = data['course']#string


    try:
        to_remove = Learning_Journey_Courses.query.filter_by(course_id=course, lj_id=id).first()
        
        #for list cases
        # uncomment if you pass in list of courses
        # courses = Learning_Journey_Courses.query.filter_by(lj_id=id).all()
        # for c in courses:
        #     if c.course_id in course:
        #         db.session.delete(c)
        
        db.session.delete(to_remove)

        #do not comment no matter is string of course or list of courses
        db.session.commit()

        # uncomment if you pass in list of courses
        # return jsonify({
        #     "message": "courses have been successfully removed."
        # }), 200

        return jsonify({
            "message": course + " have been successfully removed."
        }), 200
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

@app.route("/removelearningjourney", methods=['DELETE'])
def remove_learning_journey():
    data = request.get_json()
    id = data['lj_id']
    title = data['title']#string
    to_remove = Learning_Journey.query.filter_by(lj_id=id).first()
    if not to_remove:
        return jsonify({
            "message": title + "does not exist in database."
        }), 404

    try: 
        db.session.delete(to_remove)
        db.session.commit()

        return jsonify({
            "message": title + " have been successfully removed."
        }), 200
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

# View all learning journeys
@app.route("/viewlearningjourney")
def viewLearningJourney():
    data = request.get_json()
    id = data['staff_id']
    data = Learning_Journey.query.filter_by(staff_id=id).all()
    return jsonify(
        {
            "data": [learningJourney.to_dict() for learningJourney in data]
        }
    ), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)