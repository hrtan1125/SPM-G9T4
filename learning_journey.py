
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import *
from roles import *
from skills import *
import json
import math

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

    def calculate_progress(courses):
        total_courses = len(courses)
        completed_courses = 0
        progress = 0
        for id in courses.keys():
            if (courses[id]["completion_status"] == 'Completed'):
                completed_courses += 1
        progress = math.floor(completed_courses/total_courses*100)
        return progress

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
    __tablename__ = 'course'
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
        'polymorphic_identity': 'registration'
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

class Staff(db.Model):
    __tablename__ = 'staff'
    Staff_ID = db.Column(db.Integer, primary_key=True)
    Staff_FName = db.Column(db.String(50))
    Staff_LName = db.Column(db.String(50))
    Dept = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Role = db.Column(db.Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
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

# check user's role
@app.route("/checkrole", methods=['GET'])
def checkRole():
    try:
        staff_id = request.args.get('staff_id')
        # print(staff_id)
        staff_role = Staff.query.filter_by(Staff_ID=staff_id).first()
        # print(staff_id)
        if staff_role:
            staff_rid = staff_role.Role
            staff_dept = staff_role.Dept
            staff_name = staff_role.Staff_FName + " " + staff_role.Staff_LName
            return jsonify({
                "role": staff_rid,
                "dept": staff_dept,
                "name": staff_name,
                "staff_id" : staff_id
            }),200
        else:
            return jsonify({
                "message": "Invalid staff ID!"
            }),400
    except Exception:
        return jsonify({
            "message": "Unexpected Error"
        }),500

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

            if LearningJourneys:
                learningjourneys = [learningjourney for learningjourney in LearningJourneys]
                for learningjourney in learningjourneys:
                    # temp_dict = view_learningjourney_By_LJid(learningjourney,staff_id)
                    res = view_learningjourney_By_LJid(learningjourney,staff_id)
                    my_dict[learningjourney.lj_id] = json.loads(res[0].data)
                    
                return jsonify({
                    "data" : my_dict
                }), 200
            else:
                return jsonify({
                    "message": "No learning journeys records found."
                }), 400
            
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

#View learning journey by LJ id
@app.route("/viewlearningjourneyByLJid")
def view_learningjourney_By_LJid(learningjourney=null,staff_id=0):

    if "lj_id" in request.args:
        lj_id=request.args.get('lj_id')

        staff_id=request.args.get('staff_id')
        learningjourney = Learning_Journey.query.filter_by(lj_id=lj_id).first()
        print(learningjourney)
        print(staff_id)
    try:
        response = viewCoursesByLearningJourney(learningjourney.lj_id,staff_id)
        lj_courses_and_status = json.loads(response[0].data)
        print("courses",lj_courses_and_status)
        role = Roles.query.filter_by(role_id = learningjourney.role_id).first()
        lj_courses_and_status["title"] = learningjourney.title
        lj_courses_and_status["role_id"] = learningjourney.role_id
        lj_courses_and_status["role_name"] = role.role_name
        
        lj_courses_and_status["staff_id"] = learningjourney.staff_id
        return jsonify(lj_courses_and_status),200
       
    except Exception:
        return jsonify({
            "message": "Unable to view learning journey details."
        }), 500

# View Courses Statuses and progress
@app.route("/viewcoursesstatuses")
def view_courses_status_by_courses_ids(courses_ids_list,staff_id):
    try:
        coursesList = Courses.query.filter(Courses.course_id.in_(courses_ids_list)).all()
        # course_names = [course.course_name for course in coursesList]
        courses_dict = {course.course_id:{"course_name":course.course_name,"completion_status":""} for course in coursesList}
        courses_progress_list = Registration.query.filter(Registration.course_id.in_(courses_ids_list),Registration.staff_id==staff_id).all()
        
        for progress in courses_progress_list:
            courses_dict[progress.course_id]["completion_status"] = progress.completion_status
        final_progress = Learning_Journey_Courses.calculate_progress(courses_dict)
        return jsonify({"courses" : courses_dict, "progress": final_progress}), 200
    except Exception:
        return jsonify({
            "message": "The total number of courses is currently 0."
        }), 500
         
# view courses by learning journey
@app.route("/viewCoursesByLearningJourney", methods=['GET'])
def viewCoursesByLearningJourney(lj_id="",staff_id=0):
    if lj_id == "":
        lj_id = request.args.get('lj_id')
        staff_id=request.args.get('staff_id')
    try:
        if lj_id:
            LJcourses = Learning_Journey_Courses.query.filter_by(lj_id=lj_id).all()
            courses = [course.course_id for course in LJcourses]
            courses_and_progress = view_courses_status_by_courses_ids(courses,staff_id)
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
    print("hello adding")
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
        }), 200
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
        
@app.route("/removelearningjourney/<int:id>", methods=['DELETE'])
def remove_learning_journey(id):
    to_remove = Learning_Journey.query.filter_by(lj_id=id).first()
    if not to_remove:
        return jsonify({
            "message": "Learning Journey not found."
        }), 404
    try: 
        db.session.delete(to_remove)
        # print(id)
        db.session.commit()
        print(id)
        return jsonify({
            "message": "Learning Journey has been removed successfully."
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

@app.route("/viewTeamMembers", methods=['GET'])
def viewTeamMembers(dept='',staffid=''):
    # if request.get_json():
    #     data = request.get_json()
    #     dept =  data['dept']
    if "dept" in request.args and "staff_id" in request.args:
        dept = request.args["dept"]
        staffid = request.args["staff_id"]
    try:
        if dept and staffid:
            team_members = Staff.query.filter(Staff.Staff_ID != staffid).filter_by(Dept=dept).all()
            
            return jsonify(
                {
                    "data": [team_member.to_dict() for team_member in team_members]
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


@app.route("/viewTeamlearningjourneys", methods=['GET'])
def viewTeamlearningjourneys():
    dept = request.args.get('dept')
    my_dict = {}

    try:
        if dept:
            team_members = Staff.query.filter_by(Dept=dept).all()
            team_mems = [team_mem for team_mem in team_members]
            for team_mem in team_mems:
                print("team member is ",team_mem.Staff_ID)
                LearningJourneys = Learning_Journey.query.filter_by(staff_id=team_mem.Staff_ID).all()
                learningjourneys = [learningjourney for learningjourney in LearningJourneys]

                for learningjourney in learningjourneys:
                    res = view_learningjourney_By_LJid(learningjourney,team_mem.Staff_ID)
                    print("response data",res[0].data)
                    my_dict[learningjourney.lj_id] = json.loads(res[0].data)

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
        
@app.route("/AdminViewLearners", methods=['GET'])
def adminViewLearners():
    staff_id=request.args.get('staff_id')
    my_list = []
    try:
        if staff_id:
            staff = Staff.query.all()
            for i in staff:
                obj_Staff_Id = i.Staff_ID
                admin_Staff_Id = int(staff_id)
                if obj_Staff_Id != admin_Staff_Id:
                    my_list.append(i)
            return jsonify({
                "data" : [learner.to_dict() for learner in my_list]
            }), 200
        else:
            return jsonify({
                "message": "There are no learners available"
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)