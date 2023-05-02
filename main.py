### imports
from sys import exc_info

from flask import request, abort, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from config import app, db
from models import Instructor, Course, Instrument, InstructorCourseRelationship, InstructorInstrumentRelationship

### app config

migrate = Migrate(app, db)

# initialize flask-CORS
CORS(app)

# setup CORS headers
@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS'
    )
    return response   

### controllers


@app.route("/")
def test():
    return "all is working"

#### get requests

##### instruments

@app.route('/instruments')
def get_instruments():
    instruments = []
    try:
        instrument_query = db.paginate(db.select(Instrument).order_by(Instrument.id), per_page=10)
        if instrument_query is None:
            abort(404)
        
        for instrument in instrument_query:
            instruments.append(instrument.instrument)

    except:
        print(exc_info())
        abort(500)

    return jsonify({
        'success': True,
        'instruments': instruments
    })

@app.route('/instruments/<int:instrument_id>')
def get_individual_instrument(instrument_id):
    try:
        instrument = db.session.execute(db.select(Instrument).where(Instrument.id == instrument_id)).one_or_none()
        if instrument is None:
            abort(404)

        id = instrument[0].id
        name = instrument[0].instrument

        instructors = {}
        instructors_query = db.session.execute(db.select(Instructor).join(InstructorInstrumentRelationship).where(
                InstructorInstrumentRelationship.instrument_id == id
            )
        )
        for instructor in instructors_query:
            instructors[instructor[0].id] = instructor[0].name_short()

        if len(instructors) == 0:
            instructors = f"There are currently no {name} instructors"

        courses = {}
        courses_query = db.session.execute(db.select(Course).join(Instrument).where(Course.instrument_id == id))
        for course in courses_query:
            courses[course[0].id] = course[0].name

        if len(courses) == 0:
            courses = f"There are currently no {name} courses"
    
    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'instrument id': id,
        'instrument': name,
        'instructors': instructors,
        'courses': courses
    })

##### instructors

@app.route('/instructors')
def get_instructors():
    instructors = {}
    try:
        instructor_query = db.paginate(db.select(Instructor).order_by(Instructor.id), per_page=10)
        if instructor_query is None:
            abort(404)

        for instructor in instructor_query:
            instruments = []
            info = {}
            id = instructor.id
            
            instruments_query = db.session.execute(
                db.select(Instrument).join(InstructorInstrumentRelationship).where(
                    InstructorInstrumentRelationship.instructor_id == id
                )
            )
            
            for instrument in instruments_query:
                instruments.append(instrument[0].instrument)

            info['instructor'] = instructor.name_short()
            info['instruments'] = instruments
            instructors[id] = info
        
    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'instructors': instructors
    })

@app.route('/instructors/<int:instructor_id>')
def get_individual_instructor(instructor_id):
    try:
        instructor = db.session.execute(db.select(Instructor).where(Instructor.id == instructor_id)).one_or_none()
        if instructor is None:
            abort(404)

        id = instructor[0].id
        name = instructor[0].name()
        workdays = instructor[0].schedule

        instruments = {}
        instruments_query = db.session.execute(
            db.select(Instrument).join(InstructorInstrumentRelationship).where(
                InstructorInstrumentRelationship.instructor_id == id
            )
        )
        for instrument in instruments_query:
            instruments[instrument[0].id] = instrument[0].instrument

        courses = {}
        courses_query = db.session.execute(
            db.select(Course).join(InstructorCourseRelationship).where(
                InstructorCourseRelationship.instructor_id == id
            )
        )
        for course in courses_query:
            courses[course[0].id] = course[0].name

        if len(courses) == 0:
            courses = f"{instructor[0].name_short()} is not teaching any courses currently"
    
    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'instructor id': id,
        'name': name,
        'workdays': workdays,
        'instruments': instruments,
        'courses taught': courses
    })

##### courses

@app.route('/courses')
def get_courses():
    courses = {}
    try:
        instrument_query = db.session.execute(db.select(Instrument).order_by(Instrument.id))
        if instrument_query is None:
            abort(404)
        
        for instrument in instrument_query:
            instrument_courses = {}
            id = instrument[0].id
            course_query = db.session.execute(db.select(Course).join(Instrument).where(Course.instrument_id == id).order_by(Course.id))

            for course in course_query:
                instrument_courses[course[0].id] = course[0].name

            courses[instrument[0].instrument] = instrument_courses

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({
        'success': True,
        'courses': courses
    })

@app.route('/courses/<int:course_id>')
def get_individual_course(course_id):
    try:
        course = db.session.execute(db.select(Course).where(Course.id == course_id)).one_or_none()
        id = course[0].id
        title = course[0].name
        schedule = course[0].schedule
        
        instrument_query = db.session.execute(db.select(Instrument).where(Instrument.id == course[0].instrument_id)).one_or_none()
        instrument_name = instrument_query[0].instrument
        instrument_id = course[0].instrument_id
        instrument = {'id': instrument_id, 'name': instrument_name}

        instructors = {}
        instructors_query = db.session.execute(
            db.select(Instructor).join(InstructorCourseRelationship).where(
                InstructorCourseRelationship.course_id == id
            )
        )
        for instructor in instructors_query:
            instructors[instructor[0].id] = instructor[0].name_short()

        if len(instructors) == 0:
            instructors = f"There are currently no instructors teaching {title}"

    except:
        print(exc_info())

    finally:
        db.session.close()
    return jsonify({
        'success': True,
        'id': id,
        'course title': title,
        'instrument': instrument,
        'schedule': schedule,
        'instructors': instructors
    })

### launch

if __name__ == "__main__":
    with app.app_context():
        app.debug = True
        app.run()
