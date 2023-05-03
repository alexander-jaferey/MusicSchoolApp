### imports
from sys import exc_info

from flask import request, abort, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from config import app, db
from models import (
    Instructor,
    Course,
    Instrument,
    InstructorCourseRelationship,
    InstructorInstrumentRelationship,
)

### app config

migrate = Migrate(app, db)

# initialize flask-CORS
CORS(app)


# setup CORS headers
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,POST,DELETE,PATCH,OPTIONS"
    )
    return response


### helpers

# schedule helpers
weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def format_schedule(schedule):
    try:
        formatted_schedule = []
        for day in schedule:
            short_day = day.title()[0:3]
            if short_day not in weekdays:
                raise BadInfoError(
                    {
                        "code": 422,
                        "description": "Schedule entry contains non-valid name",
                    },
                    422,
                )

            else:
                formatted_schedule.append(short_day)

    except:
        print(exc_info())
        raise BadInfoError(
            {
                "code": 422,
                "description": "Check documentation for proper schedule formatting",
            },
            422,
        )

    return formatted_schedule


# db helpers
def get_instructors_dict():
    instructors_query = db.session.execute(
        db.select(Instructor).order_by(Instructor.id)
    )
    instructors_dict = {}

    for instructor in instructors_query:
        instructors_dict[instructor[0].name()] = instructor[0].id

    return instructors_dict


def get_instruments_dict():
    instruments_query = db.session.execute(
        db.select(Instrument).order_by(Instrument.id)
    )
    instruments_dict = {}

    for instrument in instruments_query:
        instruments_dict[instrument[0].instrument] = instrument[0].id

    return instruments_dict


def get_courses_dict():
    courses_query = db.session.execute(db.select(Course).order_by(Course.id))
    courses_dict = {}

    for course in courses_query:
        courses_dict[course[0].name] = course[0].id

    return courses_dict


def check_instructors(new_instructors, instructors_dict):
    new_instructors_list = []
    try:
        for instructor in new_instructors:
            if instructor.title() not in instructors_dict:
                raise BadInfoError(
                    {
                        "code": 422,
                        "description": f"Instructor '{instructor.title()}' not in list. If this was not a mistake, add instructor first.",
                    },
                    422,
                )

            else:
                new_instructors_list.append(instructor.title())
    except:
        print(exc_info())
        raise BadInfoError(
            {
                "code": 422,
                "description": "Check documentation for proper instructors formatting",
            },
            422,
        )

    return new_instructors_list


def check_instruments(new_instruments, instruments_dict):
    new_instruments_list = []

    try:
        for instrument in new_instruments:
            if instrument.title() not in instruments_dict:
                raise BadInfoError(
                    {
                        "code": 422,
                        "description": f"Instrument '{instrument.title()}' not in list. If this was not a mistake, add instrument first.",
                    },
                    422,
                )

            else:
                new_instruments_list.append(instrument.title())

    except:
        raise BadInfoError(
            {
                "code": 422,
                "description": "Check documentation for proper instruments formatting",
            },
            422,
        )

    return new_instruments_list


def check_courses(new_courses, courses_dict):
    new_courses_list = []

    try:
        for course in new_courses:
            if course.title() not in courses_dict:
                raise BadInfoError(
                    {
                        "code": 422,
                        "description": f"Course '{course.title()}' not in list. If this was not a mistake, add course first.",
                    },
                    422,
                )

            else:
                new_courses_list.append(course.title())

    except:
        raise BadInfoError(
            {
                "code": 422,
                "description": "Check documentation for proper courses formatting",
            },
            422,
        )

    return new_courses_list


# error helpers
class BadInfoError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


### controllers

#### get requests

##### instruments


@app.route("/instruments")
def get_instruments():
    instruments = {}
    try:
        instrument_query = db.paginate(
            db.select(Instrument).order_by(Instrument.id), per_page=10
        )
        if instrument_query is None:
            abort(404)

        for instrument in instrument_query:
            instruments[instrument.id] = instrument.instrument

    except:
        print(exc_info())
        abort(500)

    return jsonify({"success": True, "instruments": instruments})


@app.route("/instruments/<int:instrument_id>")
def get_individual_instrument(instrument_id):
    try:
        instrument = db.session.execute(
            db.select(Instrument).where(Instrument.id == instrument_id)
        ).one_or_none()
        if instrument is None:
            abort(404)

        id = instrument[0].id
        name = instrument[0].instrument

        instructors = {}
        instructors_query = db.session.execute(
            db.select(Instructor)
            .join(InstructorInstrumentRelationship)
            .where(InstructorInstrumentRelationship.instrument_id == id)
        )
        for instructor in instructors_query:
            instructors[instructor[0].id] = instructor[0].name_short()

        if len(instructors) == 0:
            instructors = f"There are currently no {name} instructors"

        courses = {}
        courses_query = db.session.execute(
            db.select(Course).join(Instrument).where(Course.instrument_id == id)
        )
        for course in courses_query:
            courses[course[0].id] = course[0].name

        if len(courses) == 0:
            courses = f"There are currently no {name} courses"

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify(
        {
            "success": True,
            "instrument id": id,
            "instrument": name,
            "instructors": instructors,
            "courses": courses,
        }
    )


##### instructors


@app.route("/instructors")
def get_instructors():
    instructors = {}
    try:
        instructor_query = db.paginate(
            db.select(Instructor).order_by(Instructor.id), per_page=10
        )
        if instructor_query is None:
            abort(404)

        for instructor in instructor_query:
            instruments = []
            info = {}
            id = instructor.id

            instruments_query = db.session.execute(
                db.select(Instrument)
                .join(InstructorInstrumentRelationship)
                .where(InstructorInstrumentRelationship.instructor_id == id)
            )

            for instrument in instruments_query:
                instruments.append(instrument[0].instrument)

            info["instructor"] = instructor.name_short()
            info["instruments"] = instruments
            instructors[id] = info

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({"success": True, "instructors": instructors})


@app.route("/instructors/<int:instructor_id>")
def get_individual_instructor(instructor_id):
    try:
        instructor = db.session.execute(
            db.select(Instructor).where(Instructor.id == instructor_id)
        ).one_or_none()
        if instructor is None:
            abort(404)

        id = instructor[0].id
        name = instructor[0].name()
        workdays = instructor[0].schedule

        instruments = {}
        instruments_query = db.session.execute(
            db.select(Instrument)
            .join(InstructorInstrumentRelationship)
            .where(InstructorInstrumentRelationship.instructor_id == id)
        )
        for instrument in instruments_query:
            instruments[instrument[0].id] = instrument[0].instrument

        courses = {}
        courses_query = db.session.execute(
            db.select(Course)
            .join(InstructorCourseRelationship)
            .where(InstructorCourseRelationship.instructor_id == id)
        )
        for course in courses_query:
            courses[course[0].id] = course[0].name

        if len(courses) == 0:
            courses = (
                f"{instructor[0].name_short()} is not teaching any courses currently"
            )

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify(
        {
            "success": True,
            "instructor id": id,
            "name": name,
            "workdays": workdays,
            "instruments": instruments,
            "courses taught": courses,
        }
    )


##### courses


@app.route("/courses")
def get_courses():
    courses = {}
    try:
        instrument_query = db.paginate(
            db.select(Instrument).order_by(Instrument.id), per_page=5
        )
        if instrument_query is None:
            abort(404)

        for instrument in instrument_query:
            instrument_courses = {}
            id = instrument.id
            course_query = db.session.execute(
                db.select(Course)
                .join(Instrument)
                .where(Course.instrument_id == id)
                .order_by(Course.id)
            )

            for course in course_query:
                instrument_courses[course[0].id] = course[0].name

            courses[instrument.instrument] = instrument_courses

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({"success": True, "courses": courses})


@app.route("/courses/<int:course_id>")
def get_individual_course(course_id):
    try:
        course = db.session.execute(
            db.select(Course).where(Course.id == course_id)
        ).one_or_none()
        id = course[0].id
        title = course[0].name
        schedule = course[0].schedule

        instrument_query = db.session.execute(
            db.select(Instrument).where(Instrument.id == course[0].instrument_id)
        ).one_or_none()
        instrument_name = instrument_query[0].instrument
        instrument_id = course[0].instrument_id
        instrument = {"id": instrument_id, "name": instrument_name}

        instructors = {}
        instructors_query = db.session.execute(
            db.select(Instructor)
            .join(InstructorCourseRelationship)
            .where(InstructorCourseRelationship.course_id == id)
        )
        for instructor in instructors_query:
            instructors[instructor[0].id] = instructor[0].name_short()

        if len(instructors) == 0:
            instructors = f"There are currently no instructors teaching {title}"

    except:
        print(exc_info())

    finally:
        db.session.close()
    return jsonify(
        {
            "success": True,
            "id": id,
            "course title": title,
            "instrument": instrument,
            "schedule": schedule,
            "instructors": instructors,
        }
    )


#### delete requests


@app.route("/instruments/<int:instrument_id>", methods=["DELETE"])
def delete_instrument(instrument_id):
    try:
        instrument = db.session.execute(
            db.select(Instrument).where(Instrument.id == instrument_id)
        ).one_or_none()
        if instrument is None:
            abort(404)

        else:
            instrument[0].delete()

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({"success": True, "deleted": instrument_id})


@app.route("/instructors/<int:instructor_id>", methods=["DELETE"])
def delete_instructor(instructor_id):
    try:
        instructor = db.session.execute(
            db.select(Instructor).where(Instructor.id == instructor_id)
        ).one_or_none()
        if instructor is None:
            abort(404)

        else:
            instructor[0].delete()

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({"success": True, "deleted": instructor_id})


@app.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        course = db.session.execute(
            db.select(Course).where(Course.id == course_id)
        ).one_or_none()
        if course is None:
            abort(404)

        else:
            course[0].delete()

    except:
        print(exc_info())
        abort(500)

    finally:
        db.session.close()

    return jsonify({"success": True, "deleted": course_id})


#### post requests


@app.route("/instruments", methods=["POST"])
def add_instrument():
    try:
        body = request.get_json()

        if body is None:
            print(exc_info())
            abort(400)

    except:
        print(exc_info())
        abort(400)

    new_instrument = body.get("instrument", None)
    new_instructors = body.get("instructors", None)

    if not new_instrument:
        abort(422)

    instrument = Instrument(instrument=new_instrument.title())

    new_instructors_list = None

    if new_instructors:
        instructors_dict = get_instructors_dict()
        new_instructors_list = check_instructors(new_instructors, instructors_dict)

    instrument.insert()

    if new_instructors_list:
        for instructor in new_instructors_list:
            instructor_join = InstructorInstrumentRelationship(
                instructor_id=instructors_dict[instructor], instrument_id=instrument.id
            )
            instructor_join.insert()

    return jsonify({"success": True, "id": instrument.id})


@app.route("/instructors", methods=["POST"])
def add_instructor():
    try:
        body = request.get_json()

        if body is None:
            print(exc_info())
            abort(400)

    except:
        print(exc_info())
        abort(400)

    new_first_name = body.get("first_name", None)
    new_last_name = body.get("last_name", None)
    new_schedule = body.get("workdays", None)
    new_instruments = body.get("instruments", None)
    new_courses = body.get("courses", None)

    if not (new_first_name and new_last_name and new_schedule and new_instruments):
        abort(422)

    formatted_schedule = format_schedule(new_schedule)

    instructor = Instructor(
        first_name=new_first_name.title(),
        last_name=new_last_name.title(),
        schedule=formatted_schedule,
    )

    instruments_dict = get_instruments_dict()
    new_instruments_list = check_instruments(new_instruments, instruments_dict)

    new_courses_list = []

    if new_courses:
        courses_dict = get_courses_dict()
        new_courses_list = check_courses()

    instructor.insert()

    for instrument in new_instruments_list:
        instrument_join = InstructorInstrumentRelationship(
            instructor_id=instructor.id, instrument_id=instruments_dict[instrument]
        )
        instrument_join.insert()

    if new_courses_list:
        for course in new_courses_list:
            course_join = InstructorCourseRelationship(
                instructor_id=instructor.id, course_id=courses_dict[course]
            )
            course_join.insert()

    return jsonify({"success": True, "id": instructor.id})


@app.route("/courses", methods=["POST"])
def add_course():
    try:
        body = request.get_json()

        if body is None:
            abort(400)

    except:
        abort(400)

    new_title = body.get("title", None)
    new_instrument = body.get("instrument", None)
    new_schedule = body.get("schedule", None)
    new_instructors = body.get("instructors", None)

    if not (new_title and new_instrument and new_schedule):
        abort(422)

    formatted_schedule = format_schedule(new_schedule)

    try:
        instrument = db.session.execute(
            db.select(Instrument).where(Instrument.instrument == new_instrument.title())
        ).one_or_none()

    except:
        raise BadInfoError(
            {
                "code": 422,
                "description": f"Instrument '{new_instrument.title()}' not in list. If this was not a mistake, add instrument first.",
            },
            422,
        )

    new_instrument_id = instrument[0].id

    course = Course(
        name=new_title.title(),
        schedule=formatted_schedule,
        instrument_id=new_instrument_id,
    )

    new_instructors_list = None

    if new_instructors:
        instructors_dict = get_instructors_dict()
        new_instructors_list = check_instructors(new_instructors, instructors_dict)

    course.insert()

    if new_instructors_list:
        for instructor in new_instructors_list:
            instructor_join = InstructorCourseRelationship(
                instructor_id=instructors_dict[instructor], course_id=course.id
            )
            instructor_join.insert()

    return jsonify({"success": True, "id": course.id})


#### error handlers


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}),
        405,
    )


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "internal server error"}),
        500,
    )


@app.errorhandler(BadInfoError)
def bad_info(error):
    body = error.error
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": body["description"],
            }
        ),
        error.status_code,
    )


### launch

if __name__ == "__main__":
    with app.app_context():
        app.debug = True
        app.run()
