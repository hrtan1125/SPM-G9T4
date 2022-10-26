from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import *
from roles import *
from skills import *
import math
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
class Registration(db.Model):
    __tablename__ = 'registration'
    reg_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(50))
    staff_id = db.Column(db.Integer)
    reg_status = db.Column(db.String(15))
    completion_status = db.Column(db.String(10))
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
# view registration
@app.route("/viewAllRegistration", methods=['GET'])
def viewAllRegistration():
    try:
        registrations = Registration.query.all()
        if registrations:
            return jsonify({
                "data": [registration.to_dict() for registration in registrations]
            }), 200
        else:
            return jsonify({
                "message": "No registration available."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
        }), 500
# view learningjourneys and progress
@app.route("/viewlearningjourneys", methods=['GET'])
def viewlearningjourneys():
    staff_id = request.args.get('staff_id')
    my_dict = {}
    try:
        if staff_id:
            LearningJourneys = Learning_Journey.query.filter_by(staff_id=staff_id).all()
            learningjourneys = [learningjourney for learningjourney in LearningJourneys]
            for learningjourney in learningjourneys:
                temp_dict = view_learningjourney_By_LJid(learningjourney)
                my_dict[learningjourney.lj_id] = temp_dict
                
            return jsonify({
                "data" : my_dict
            }), 200
        else:
            return jsonify({
                "message": "No registration available."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
        }), 500
#View learning journey by LJ id
@app.route("/viewlearningjourneyByLJid")
def view_learningjourney_By_LJid(learningjourney):
    try:
        lj_courses_and_status = viewCoursesByLearningJourney(learningjourney.lj_id)
        role = Roles.query.filter_by(role_id = learningjourney.role_id).first()
        lj_courses_and_status["title"] = learningjourney.title
        lj_courses_and_status["role_id"] = learningjourney.role_id
        lj_courses_and_status["role_name"] = role.role_name
        
        lj_courses_and_status["staff_id"] = learningjourney.staff_id
        return lj_courses_and_status
       
    except Exception:
        return jsonify({
            "message": "Unable to view learning journey details."
        }), 500
# View Courses Statuses and progress
@app.route("/viewcoursesstatuses")
def view_courses_status_by_courses_ids(courses_ids_list):
    
    coursesList = Courses.query.filter(Courses.course_id.in_(courses_ids_list)).all()
    course_names = [course.course_name for course in coursesList]
    courses_progress_list = Registration.query.filter(Registration.course_id.in_(courses_ids_list)).all()
    
    courses_and_statuses = [[progress.completion_status, progress.course_id] for progress in courses_progress_list]
    for index in range(len(course_names)):
        courses_and_statuses[index].append(course_names[index])
    total = 0
    completed = 0
    final_progress = 0
    for course_and_status in courses_and_statuses:
        if (course_and_status[0] == 'Completed'):
            completed += 1
        total += 1
    if(total != 0):
        final_progress = math.floor(completed/total * 100)
    return {"courses" : courses_and_statuses, "progress": final_progress}
    

# view courses by learning journey
@app.route("/viewCoursesByLearningJourney", methods=['GET'])
def viewCoursesByLearningJourney(lj_id=""):
    if lj_id == "":
        lj_id = request.args.get('lj_id')
    try:
        if lj_id:
            LJcourses = Learning_Journey_Courses.query.filter_by(lj_id=lj_id).all()
            courses = [course.course_id for course in LJcourses]
            coursesList = Courses.query.filter(Courses.course_id.in_(courses),Courses.course_status=="Active").all()
            CoursesIdList = [course.course_id for course in coursesList]
            courses_and_progress = view_courses_status_by_courses_ids(CoursesIdList)
            return courses_and_progress
        else:
            return jsonify({
                "message": "No registration available."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
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
    print(data)
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
    title = data["title"]   
    to_remove = Learning_Journey.query.filter_by(lj_id=id).first()
    if not to_remove:
        return jsonify({
            "message": "Learning Journey not found."
        }), 404
    try: 
        db.session.delete(to_remove)
        db.session.commit()
        return jsonify({
            "message": title + " has been removed successfully."
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
# Filter Learning Journey(s) based on role
@app.route("/filterLearningJourneyByRole", methods=['GET'])
def filterLearningJourneyByRole():
    data = request.get_json()
    id = data['staff_id']
    role = data['role_id']
    if(Learning_Journey.query.filter_by(staff_id=id, role_id=role).all()):
        learningJourneys = Learning_Journey.query.filter_by(staff_id=id, role_id=role).all()
        return jsonify(
            {
                "data": [learningJourney.to_dict() for learningJourney in learningJourneys]
            }
        ), 200
    
    else:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "staff_id": id,
                    "role_id": role
                },
                "message": "No Learning Journey found for this role."
            }
        ), 400
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
