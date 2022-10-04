from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
                                        '@localhost:3306/learningjourneydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Learning_Journey(db.Model):
    __tablename__ = 'learningjourney'

    lj_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    role_id = db.Column(db.Integer)
    staff_id = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'learningjourney'
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
    __tablename__ = 'learningjourneycourses'

    lj_id = db.Column(db.Integer)
    skill_code = db.Column(db.String(20))
    course_id = db.Column(db.String(20))
    row_id = db.Column(db.Integer, primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'learningjourneycourses'
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


@app.route("/createlearningjourney", methods=['POST'])
def create_learningjourney():
    data = request.get_json()

    ##checking for correct data type
    if not all(key in data.keys() for
               key in ('title',
                       'role_id', 
                       'staff_id')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
    title = data["title"]
    role_id = data["role_id"]
    staff_id = data["staff_id"]
    
    learning_journey = Learning_Journey(**{"title": title,"role_id":role_id, "staff_id":staff_id})
    
    try:
        db.session.add(learning_journey)
        db.session.flush()
        db.session.commit()
        return jsonify(learning_journey.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

@app.route("/addlearningjourneycourses", methods=['POST'])
def add_learningjourneycourses():
    data = request.get_json()

    ##checking for correct data type
    if not all(key in data.keys() for
               key in ('lj_id',
                        'skill_code',
                        'course_id')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500

    ##check if learning journey already has that course (No need thanks to function in later sprint)
    lj_id = data["lj_id"]
    skill_code = data["skill_code"]
    course_id = data["course_id"]
    row_id = 11
    learning_journey_courses = Learning_Journey_Courses(**{"row_id":row_id,"lj_id": lj_id,"skill_code":skill_code, "course_id":course_id})
    # checkCourse = Learning_Journey_Courses.query.filter_by(lj_id = lj_id, course_id = course_id).first()
    # if checkRole and checkRole.deleted!="yes":
    #         return jsonify(
    #             {
    #                 "message": "This course is already in the selected learning journey!"
    #             }
    #         ), 400
    try:
        db.session.add(learning_journey_courses)
        db.session.flush()
        db.session.commit()
        return jsonify(learning_journey_courses.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
