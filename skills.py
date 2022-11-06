from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
from sqlalchemy import and_
import json

from roles import Role_Skills
# from learning_journey import * 

app = Flask(__name__)
if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
                                            '@localhost:3306/testDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                            'pool_recycle': 280}
else:
     app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


class Skills_acquired(db.Model):
    __tablename__ = 'skills_acquired'
    row_id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(20))
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

    def __init__(self, staff_id, skill_code):
        self.staff_id = staff_id
        self.skill_code = skill_code


@app.route("/create", methods=['POST'])  #create skill
def create_skill():
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('skill_code', "skill_name")):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
    new_skill = data["skill_name"]
    new_code = data['skill_code']
    check_skill = Skills.query.filter_by(skill_name=new_skill, deleted="no").first()
    check_skill_code = Skills.query.filter_by(skill_code=new_code, deleted="no").first()
    if check_skill and check_skill_code:
            return jsonify(
                {
                    "message": "Skill code and name already exist!"
                }
            ), 400
    elif check_skill:    
        return jsonify(
                {
                    "message": "Skill name already exist!"
                }), 400
    elif check_skill_code:
        return jsonify(
            {
                "message": "Skill code already exist!"
            }
        ),400
    data['deleted']='no'
    skill = Skills(**data)
    try:
        db.session.add(skill)
        db.session.commit()
        return jsonify({"data": [{"skill created": skill.to_dict()}, {"message": "Skill created successfully."}]}), 201
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
        skill_list = Skills.query.filter_by(deleted="no").all()
    return jsonify(
        {
            "data": [skill.to_dict() for skill in skill_list]
        }
    ), 200

# admin read all skills
@app.route("/viewselectedskill", methods=['GET'])
def viewSelectedSkill():
    try:
        skill_code = request.args["skill_code"]
        selectedSkill = Skills.query.filter_by(skill_code=skill_code).first()
        return jsonify(selectedSkill.to_dict()), 201
    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        )

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
    try:
        data = request.get_json()
        skill_code = data["skill_code"]
        skillToDelete = Skills.query.filter_by(skill_code=skill_code, deleted="no").first()
        if skillToDelete:
            skillToDelete.deleted = "yes"
            db.session.commit()
            return jsonify({
                "message": "Skill has been removed!"
            }),200
        
        return jsonify({
            "message": "Skill no longer available."
        }), 400

    except Exception:
        return jsonify(
            {
                "message": "Unexpected Error."
            }
        ),400

### assign course start here###
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
        ),200
    return jsonify(
        {
            "code": 404, 
            "message": "There is no entry"
        }
    ), 404

#list all skills available to be added to the course
#check if the skills already assigned to the course
#split out the skills which already assigned
@app.route("/view_skills_to_add/<id>", methods=['GET'])
def view_skills_to_add(id):
    try:
        assigned_skills = Course_skills.query.filter_by(course_id=id).all()
        skills = [skill.skill_code for skill in assigned_skills]

        if skills:
            return jsonify({
                "skills":skills
                }), 200
        else: 
            return jsonify({
                "message": "no skills assigned to the course yet."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit database."
        }), 500
    


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
    
    skills = data['skills'] #list

    try:
        
        for skill in skills:
            #check if the combination of course and skill exists
            if (Course_skills.query.filter_by(course_id=course_id, skill_code=skill).first()):
                return jsonify(
                    {
                        "message": "skill for this course already exist"
                    }),400
            course_skill = Course_skills(course_id, skill)
            db.session.add(course_skill)
        db.session.commit()         

    except SQLAlchemyError as e:
        print(e)

    return jsonify(
            {
              "message": "Course and Skills successfully updated"
            }),200

@app.route("/viewRoleSkills", methods=['GET'])
def viewRoleSkills():
    search_skill = request.args.get('role_id')
    try:
        if search_skill:
            RoleSkills = Role_Skills.query.filter_by(role_id=search_skill).all()
            skills = viewSkillsByRole(RoleSkills)

            return skills
        else:
            return jsonify({
                "message": "Missing Input."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

def viewSkillsByRole(RoleSkills=[]):
    try:
        if RoleSkills:
            skills = [skill.skill_code for skill in RoleSkills]
            skillslist = Skills.query.filter(and_(Skills.skill_code.in_(skills),Skills.deleted=="no")).all()
            print([skill.skill_code for skill in skillslist])
            return jsonify({
                "data": {skill.skill_code:skill.to_dict() for skill in skillslist}
            }), 200
        else:
            return jsonify({
                "message": "Missing Input."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

# need to add skill name 
@app.route("/viewTeamMembersSkills", methods=['GET'])
def managerViewTeamMembersSkills(dept='',staffid=''):

    from learning_journey import viewTeamMembers
    # {
    #     dept:'Ops'
    # }

    if request.get_json():
        data = request.get_json()
        dept =  data['dept']
        staffid = data['staff_id']

    
    if "dept" in request.args:
        dept = request.args.get("dept")
        staffid = request.args.get("staff_id")
    
    try: 

        # get the the list of team members
        team_members_json = viewTeamMembers(dept, staffid)
        team_members = json.loads(team_members_json[0].data)
        team_members_list = team_members["data"]

        my_list = []
        for team_member in team_members_list:
            if team_member['Role'] != 3:
                my_list.append(team_member['Staff_ID'])
            # return jsonify(my_list) 

        all_list = Skills_acquired.query.filter(Skills_acquired.staff_id.in_(my_list)).all()
        skills_acquired_list = [code.to_dict() for code in all_list]
        skills_list = [skill.skill_code for skill in all_list]
            # return jsonify(skills_acquired_list) 

        empty_dict = {}
        skills_dict = viewSkillsByCodes(skills_list)
        for skills_acquired_obj in skills_acquired_list:
            sc = skills_acquired_obj["skill_code"]
            if skills_acquired_obj['staff_id'] in empty_dict.keys():
                empty_dict[skills_acquired_obj['staff_id']][sc] = skills_dict[sc]
            else:
                # empty_dict[skills_acquired_list]
                empty_dict[skills_acquired_obj['staff_id']]= {sc:skills_dict[sc]}
        return jsonify({
                "data" : empty_dict
            }), 200
    
    except Exception:
        return jsonify({
            "message": "Unexpected Error."
        }), 500

def viewSkillsByCodes(skill_code_list):
    try:
        print("h1")
        my_skills = Skills.query.filter(and_(Skills.skill_code.in_(skill_code_list),Skills.deleted=="no")).all()
        print("h2")
        skills_dict = {skill.skill_code:skill.skill_name for skill in my_skills}
        print(skills_dict)
        return skills_dict
    except Exception:
        return jsonify({
            "message": "Unexpected Error."
        }), 500

#Admin views Learner's Skills Function
@app.route("/viewLearnersSkills", methods=['GET'])
def viewLearnersSkills():
    # from learning_journey import Staff
    # receivedRequest = request.json
    # staff_id = receivedRequest["staff_id"]
    staff_id = request.args.get('staff_id')
    skill_list = []
    # my_dict = {}
    try:
        
        # staff = Staff.query.filter_by(Staff_ID=staff_id).first()
        # staff_role = staff.Role
        temp = Skills_acquired.query.filter_by(staff_id=staff_id).all()
        for item in temp:
            skill = item.skill_code
            skill_dict=viewSkillsByCodes([skill])
            skill_list.append(skill_dict)
        # my_dict = viewSkillsByCodes(skill_list)
        if skill_list:
            return jsonify({
                "data" : skill_list
            }), 200
        else:
            return jsonify({
                "message": "No staffID."
            }), 400
    except Exception:
        return jsonify({
            "message": "Unable to commit to database"
        }), 500

@app.route("/viewTeamMembersCourses", methods=['GET'])
def managerViewTeamMembersCourses(dept='',staffid=''):

    from learning_journey import Registration, Courses

    if request.get_json():
        data = request.get_json()
        dept =  data['dept']
        staffid = data['staff_id']
    

    print ("hello")

    
    try:
        print(staffid, dept)
        team_members_skills_json = managerViewTeamMembersSkills(dept, staffid)
        team_members_skill = json.loads(team_members_skills_json[0].data)
        team_members_skill_obj = team_members_skill["data"]
        # return jsonify(team_members_skill_obj)

        empty_dict = {}
        for member_id in team_members_skill_obj.keys():
            reg_list_from_staff_id = Registration.query.filter_by(staff_id=member_id, completion_status ='Completed').all()
            staff_roles = [reg.to_dict() for reg in reg_list_from_staff_id]
            empty_dict[member_id] = staff_roles

        name_temp_dict = {}
        for member_obj in empty_dict:
            for attr in empty_dict[member_obj]:
                course_id = attr['course_id']
                course = Courses.query.filter_by(course_id=course_id).first()
                course_id = course.course_id
                course_name = course.course_name
                name_temp_dict[course_id] = course_name

        for member_obj in empty_dict:
            list_of_obj = empty_dict[member_obj]
            for obj in list_of_obj:
                if obj['course_id'] in name_temp_dict.keys():
                    course_id = obj['course_id']
                    obj['course_name'] = name_temp_dict[course_id]

        return jsonify({
                    "data" : empty_dict
                }), 200
    
    except Exception:
        return jsonify({
            "message": "Unexpected Error."
        }), 500


#Admin remove skills from course
@app.route("/course_remove_skills", methods=['DELETE'])
def course_remove_skills():
    #check if exists
    data = request.get_json() #py obj
    course_id = data['course_id']
    
    skills = data['skills'] #list

    if(skills == []):
        return jsonify(
        {
            "code": 201,
            "message": "No skill removed from role"
        }
    ), 201

    courseSkillsRecords = Course_skills.query.filter_by(course_id=course_id).all()
    numOfRecords = len(courseSkillsRecords)
    # for record in courseSkillsRecords:
    #     numOfRecords +=1

    if(numOfRecords == len(skills)):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "skill_code": skills,
                        "course_id": course_id
                    },
                    "message": "Skill cannot be removed. A course must have at least one skill."
                }
            ), 400

    else:
        for skill in skills:            
            courseSkill = Course_skills.query.filter_by(skill_code=skill, course_id=course_id).first()
            if (courseSkill):
                try:
                    db.session.delete(courseSkill)
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
                                "course_id": course_id
                            },
                            "message": "An error occurred when removing skill from course."
                        }
                    ), 500

    return jsonify(
        {
            "code": 201,
            "message": "Successful removal of skill(s) from course"
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
