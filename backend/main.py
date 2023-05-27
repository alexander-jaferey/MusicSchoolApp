### imports
from sys import exc_info

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from config import db_url
from auth.auth import requires_auth, AuthError
from db.models import (
    db,
    Instructor,
    Course,
    Instrument,
    InstructorCourseRelationship,
    InstructorInstrumentRelationship,
)
def create_app(test_config=None):
    ### app config
    app = Flask("music_school_api")
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_url
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

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

    #### schedule helpers
    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    ##### schedule formatter to keep database consistent


    def format_schedule(schedule):
        if type(schedule) is not list:
            print(exc_info())
            raise BadInfoError(
                {
                    "code": 422,
                    "description": "Check documentation for proper schedule formatting",
                },
                422,
            )

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

        return formatted_schedule


    #### db helpers

    ##### create dictionary with instructors info


    def get_instructors_dict():
        instructors_query = db.session.execute(
            db.select(Instructor).order_by(Instructor.id)
        )
        instructors_dict = {}

        for instructor in instructors_query:
            instructors_dict[instructor[0].name()] = instructor[0].id

        return instructors_dict


    ##### create dictionary with instruments info


    def get_instruments_dict():
        instruments_query = db.session.execute(
            db.select(Instrument).order_by(Instrument.id)
        )
        instruments_dict = {}

        for instrument in instruments_query:
            instruments_dict[instrument[0].instrument] = instrument[0].id

        return instruments_dict


    ##### create dictionary with courses info


    def get_courses_dict():
        courses_query = db.session.execute(db.select(Course).order_by(Course.id))
        courses_dict = {}

        for course in courses_query:
            courses_dict[course[0].name] = course[0].id

        return courses_dict


    ##### check a list of instructor names against the database and create dict with names and ids


    def check_instructors(new_instructors, instructors_dict):
        if type(new_instructors) is not list:
            print(exc_info())
            raise BadInfoError(
                {
                    "code": 422,
                    "description": "Check documentation for proper instructors formatting",
                },
                422,
            )

        new_instructors_list = []
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

        return new_instructors_list


    ##### check a list of instrument names against the database and create dict with names and ids


    def check_instruments(new_instruments, instruments_dict):
        if type(new_instruments) is not list:
            print(exc_info())
            raise BadInfoError(
                {
                    "code": 422,
                    "description": "Check documentation for proper instruments formatting",
                },
                422,
            )

        new_instruments_list = []
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

        return new_instruments_list


    ##### check a list of course names against the database and create dict with names and ids


    def check_courses(new_courses, courses_dict):
        if type(new_courses) is not list:
            raise BadInfoError(
                {
                    "code": 422,
                    "description": "Check documentation for proper courses formatting",
                },
                422,
            )

        new_courses_list = []
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

        return new_courses_list


    ##### create dicts for later use
    with app.app_context():
        instructors_dict = get_instructors_dict()
        instruments_dict = get_instruments_dict()
        courses_dict = get_courses_dict()

    ##### set null variables

    new_instruments_list = None
    new_instructors_list = None
    new_courses_list = None
    removed_instruments_list = None
    removed_instructors_list = None
    removed_courses_list = None

    #### error helpers

    ##### error class to give more information when a request has invalid info


    class BadInfoError(Exception):
        def __init__(self, error, status_code):
            self.error = error
            self.status_code = status_code


    ### controllers

    #### tests

    # @app.route("/schedule-test", methods=["POST"])
    # def test_schedules():
    # body = request.get_json()
    # schedule = body.get("schedule")
    # print(format_schedule(schedule))

    # return jsonify({"success": True})

    #### get requests

    ##### instruments


    @app.route("/instruments")
    def get_instruments():
        instruments = {}
        try:
            # get paginated list of instruments
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

        return jsonify(
            {
                "success": True,
                "instruments": instruments,
                "total_instruments": instrument_query.total,
                "current_page": instrument_query.page,
                "total_pages": instrument_query.pages,
            }
        )


    @app.route("/instruments/<int:instrument_id>")
    @requires_auth("get:instruments")
    def get_individual_instrument(payload, instrument_id):
        # get instrument by provided id
        instrument = db.one_or_404(
            db.select(Instrument).where(Instrument.id == instrument_id)
        ).one_or_none()

        try:
            id = instrument[0].id
            name = instrument[0].instrument

            instructors = {}
            # get all instructors associated with this instrument
            instructors_query = db.session.execute(
                db.select(Instructor)
                .join(InstructorInstrumentRelationship)
                .where(InstructorInstrumentRelationship.instrument_id == id)
            )
            for instructor in instructors_query:
                instructors[instructor[0].id] = instructor[0].name_short()

            # provide friendly text if no instructors are found
            if len(instructors) == 0:
                instructors = f"There are currently no {name} instructors"

            courses = {}
            # get all courses associated with this instrument
            courses_query = db.session.execute(
                db.select(Course).join(Instrument).where(Course.instrument_id == id)
            )
            for course in courses_query:
                courses[course[0].id] = course[0].name

            # provide friendly text if no courses are found
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
            # get paginated list of instructors
            instructor_query = db.paginate(
                db.select(Instructor).order_by(Instructor.id), per_page=8
            )
            if instructor_query is None:
                abort(404)

            # create dict object with name and instruments for each instructor
            for instructor in instructor_query:
                instruments = []
                info = {}
                id = instructor.id

                # get all instruments associated with this instructor
                instruments_query = db.session.execute(
                    db.select(Instrument)
                    .join(InstructorInstrumentRelationship)
                    .where(InstructorInstrumentRelationship.instructor_id == id)
                )

                for instrument in instruments_query:
                    instruments.append(instrument[0].instrument)

                info["instructor"] = instructor.name_short()
                info["instruments"] = instruments
                # add individual instructor dict to main dict
                instructors[id] = info

        except:
            print(exc_info())
            abort(500)

        finally:
            db.session.close()

        return jsonify(
            {
                "success": True,
                "instructors": instructors,
                "total_instructors": instructor_query.total,
                "current_page": instructor_query.page,
                "total_pages": instructor_query.pages,
            }
        )


    @app.route("/instructors/<int:instructor_id>")
    @requires_auth("get:instructors")
    def get_individual_instructor(payload, instructor_id):
        # get instructor by provided id
        instructor = db.one_or_404(
            db.select(Instructor).where(Instructor.id == instructor_id)
        ).one_or_none()

        try:
            id = instructor[0].id
            name = instructor[0].name()
            workdays = instructor[0].schedule

            instruments = {}
            # get all instruments associated with this instructor
            instruments_query = db.session.execute(
                db.select(Instrument)
                .join(InstructorInstrumentRelationship)
                .where(InstructorInstrumentRelationship.instructor_id == id)
            )
            for instrument in instruments_query:
                instruments[instrument[0].id] = instrument[0].instrument

            courses = {}
            # get all courses associated with this instructor
            courses_query = db.session.execute(
                db.select(Course)
                .join(InstructorCourseRelationship)
                .where(InstructorCourseRelationship.instructor_id == id)
            )
            for course in courses_query:
                courses[course[0].id] = course[0].name

            # provide friendly text if no courses are found
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
            # get paginated list of instruments
            instrument_query = db.paginate(
                db.select(Instrument).order_by(Instrument.id),
                per_page=5,
            )
            if instrument_query is None:
                abort(404)

            # create dict object with courses for each instrument
            for instrument in instrument_query:
                instrument_courses = {}
                id = instrument.id
                # get all courses associated with this instrument
                course_query = db.session.execute(
                    db.select(Course)
                    .join(Instrument)
                    .where(Course.instrument_id == id)
                    .order_by(Course.id)
                )

                for course in course_query:
                    instrument_courses[course[0].id] = course[0].name

                # add individual course dict to main dict
                courses[instrument.instrument] = instrument_courses

        except:
            print(exc_info())
            abort(500)

        finally:
            db.session.close()

        return jsonify(
            {
                "success": True,
                "courses": courses,
                "total_instruments": instrument_query.total,
                "current_page": instrument_query.page,
                "total_pages": instrument_query.pages,
            }
        )


    @app.route("/courses/<int:course_id>")
    @requires_auth("get:courses")
    def get_individual_course(payload, course_id):
            # get course by provided id
        course = db.one_or_404(
            db.select(Course).where(Course.id == course_id)
        ).one_or_none()

        try:
            id = course[0].id
            title = course[0].name
            schedule = course[0].schedule

            # get instrument associated with this course
            instrument_query = db.session.execute(
                db.select(Instrument).where(Instrument.id == course[0].instrument_id)
            ).one_or_none()
            instrument_name = instrument_query[0].instrument
            instrument_id = course[0].instrument_id
            instrument = {"id": instrument_id, "name": instrument_name}

            instructors = {}
            # get all instructors associated with this course
            instructors_query = db.session.execute(
                db.select(Instructor)
                .join(InstructorCourseRelationship)
                .where(InstructorCourseRelationship.course_id == id)
            )
            for instructor in instructors_query:
                instructors[instructor[0].id] = instructor[0].name_short()

            # provide friendly text if no instructors are found
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
    @requires_auth("delete:instruments")
    def delete_instrument(payload, instrument_id):
        # get instrument by provided id
        instrument = db.one_or_404(
            db.select(Instrument).where(Instrument.id == instrument_id)
        ).one_or_none()
        try:
            instrument[0].delete()

        except:
            print(exc_info())
            abort(500)

        finally:
            db.session.close()

        return jsonify({"success": True, "deleted": instrument_id})


    @app.route("/instructors/<int:instructor_id>", methods=["DELETE"])
    @requires_auth("delete:instructors")
    def delete_instructor(payload, instructor_id):
        # get instructor by provided id
        instructor = db.one_or_404(
            db.select(Instructor).where(Instructor.id == instructor_id)
        ).one_or_none()

        try:
            instructor[0].delete()

        except:
            print(exc_info())
            abort(500)

        finally:
            db.session.close()

        return jsonify({"success": True, "deleted": instructor_id})


    @app.route("/courses/<int:course_id>", methods=["DELETE"])
    @requires_auth("delete:courses")
    def delete_course(payload, course_id):
        # get course by provided id
        course = db.one_or_404(
            db.select(Course).where(Course.id == course_id)
        ).one_or_none()

        try:
            course[0].delete()

        except:
            print(exc_info())
            abort(500)

        finally:
            db.session.close()

        return jsonify({"success": True, "deleted": course_id})


    #### post requests


    @app.route("/instruments", methods=["POST"])
    @requires_auth("post:instruments")
    def add_instrument(payload):
        try:
            # get request body
            body = request.get_json()

            if body is None:
                print(exc_info())
                abort(400)

        except:
            print(exc_info())
            abort(400)

        new_instrument = body.get("instrument", None)
        new_instructors = body.get("instructors", None)

        new_instructors_list = None

        # error out if no instrument name is provided
        if not new_instrument:
            abort(422)

        # create new instrument object with provided name
        instrument = Instrument(instrument=new_instrument.title())

        # check list of instructors against database and create dict with names and ids
        if new_instructors:
            new_instructors_list = check_instructors(new_instructors, instructors_dict)

        try:
            # add instrument to database
            instrument.insert()

        except IntegrityError:
            # throw error for duplicate name
            raise BadInfoError(
                {"code": 422, "description": "An instrument by that name already exists!"},
                422,
            )

        if new_instructors_list:
            # add rows to association table for each instructor in dict
            for instructor in new_instructors_list:
                instructor_join = InstructorInstrumentRelationship(
                    instructor_id=instructors_dict[instructor], instrument_id=instrument.id
                )
                instructor_join.insert()

        return jsonify({"success": True, "id": instrument.id})


    @app.route("/instructors", methods=["POST"])
    @requires_auth("post:instructors")
    def add_instructor(payload):
        try:
            # get request body
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

        new_instruments_list = None
        new_courses_list = None

        # error out if required fields are not provided
        if not (new_first_name and new_last_name and new_schedule and new_instruments):
            abort(422)

        formatted_schedule = format_schedule(new_schedule)

        # create new instructor object with provided info
        instructor = Instructor(
            first_name=new_first_name.title(),
            last_name=new_last_name.title(),
            schedule=formatted_schedule,
        )

        # check list of instruments against database and create dict with names and ids
        new_instruments_list = check_instruments(new_instruments, instruments_dict)

        if new_courses:
            # check list of coourses against database and create dict with names and ids
            new_courses_list = check_courses()

        try:
            # add instructor to database
            instructor.insert()

        except IntegrityError:
            # throw error for duplicate name
            raise BadInfoError(
                {"code": 422, "description": "An instructor by that name already exists!"},
                422,
            )

        for instrument in new_instruments_list:
            # add rows to association table for each instrument in dict
            instrument_join = InstructorInstrumentRelationship(
                instructor_id=instructor.id, instrument_id=instruments_dict[instrument]
            )
            instrument_join.insert()

        if new_courses_list:
            for course in new_courses_list:
                # add rows to association table for each course in dict
                course_join = InstructorCourseRelationship(
                    instructor_id=instructor.id, course_id=courses_dict[course]
                )
                course_join.insert()

        return jsonify({"success": True, "id": instructor.id})


    @app.route("/courses", methods=["POST"])
    @requires_auth("post:courses")
    def add_course(payload):
        try:
            # get request body
            body = request.get_json()

            if body is None:
                abort(400)

        except:
            abort(400)

        new_title = body.get("title", None)
        new_instrument = body.get("instrument", None)
        new_schedule = body.get("schedule", None)
        new_instructors = body.get("instructors", None)

        new_instructors_list = None

        # error out if required fields are not provided
        if not (new_title and new_instrument and new_schedule):
            abort(422)

        formatted_schedule = format_schedule(new_schedule)

        # get instrument id
        try:
            instrument = db.session.execute(
                db.select(Instrument).where(Instrument.instrument == new_instrument.title())
            ).one_or_none()

        except:
            # throw error if instrument not found
            raise BadInfoError(
                {
                    "code": 422,
                    "description": f"Instrument '{new_instrument.title()}' not in list. If this was not a mistake, add instrument first.",
                },
                422,
            )

        new_instrument_id = instrument[0].id

        # create new course object with provided info
        course = Course(
            name=new_title.title(),
            schedule=formatted_schedule,
            instrument_id=new_instrument_id,
        )

        if new_instructors:
            # check list of instructors against database and create dict with names and ids
            instructors_dict = get_instructors_dict()
            new_instructors_list = check_instructors(new_instructors, instructors_dict)

        try:
            # add course to database
            course.insert()

        except IntegrityError:
            # throw error for duplicate name
            raise BadInfoError(
                {"code": 422, "description": "A course by that name already exists!"},
                422,
            )

        if new_instructors_list:
            for instructor in new_instructors_list:
                # add rows to association table for each instructor in dict
                instructor_join = InstructorCourseRelationship(
                    instructor_id=instructors_dict[instructor], course_id=course.id
                )
                instructor_join.insert()

        return jsonify({"success": True, "id": course.id})


    #### patch requests


    @app.route("/instruments/<int:instrument_id>", methods=["PATCH"])
    @requires_auth("patch:instruments")
    def update_instrument(payload, instrument_id):
        # get instrument by provided id
        instrument_query = db.one_or_404(
            db.select(Instrument).where(Instrument.id == instrument_id)
        ).one_or_none()

        instrument = instrument_query[0]

        try:
            # get request body
            body = request.get_json()

            if body is None:
                abort(400)

        except:
            abort(400)

        new_name = body.get("instrument", None)
        new_instructors = body.get("new_instructors", None)
        removed_instructors = body.get("removed_instructors", None)

        new_instructors_list = None

        if new_name:
            # update name if provided
            instrument.instrument = new_name.title()

        if new_instructors:
            # check list of instructors, if provided, against database and create dict with names and ids
            new_instructors_list = check_instructors(new_instructors, instructors_dict)

        if new_instructors_list:
            # add rows to association table for each instructor in dict
            for instructor in new_instructors_list:
                instructor_join = InstructorInstrumentRelationship(
                    instructor_id=instructors_dict[instructor], instrument_id=instrument.id
                )
                instructor_join.insert()

        if removed_instructors:
            # check list of instructors to be deassociated from instrument, if provided, against database and create dict with names and ids
            removed_instructors_list = check_instructors(
                removed_instructors, instructors_dict
            )

        if removed_instructors_list:
            # deleterows from association table for each instructor in dict
            for instructor in removed_instructors_list:
                instructor_join_query = db.session.execute(
                    db.select(InstructorInstrumentRelationship)
                    .where(
                        InstructorInstrumentRelationship.instructor_id
                        == instructors_dict[instructor]
                    )
                    .where(InstructorInstrumentRelationship.instrument_id == instrument_id)
                ).one_or_none()

                if instructor_join_query is None:
                    pass

                else:
                    instructor_join_query[0].delete()

        if new_name:
            try:
                # update instrument in database
                instrument.update()

            except IntegrityError:
                # throw error for duplicate name
                raise BadInfoError(
                    {
                        "code": 422,
                        "description": "An instrument by that name already exists!",
                    },
                    422,
                )

        return jsonify({"success": True})


    @app.route("/instructors/<int:instructor_id>", methods=["PATCH"])
    @requires_auth("patch:instructors")
    def update_instructor(payload, instructor_id):
        try:
            # get instructor by provided id
            instructor_query = db.session.execute(
                db.select(Instructor).where(Instructor.id == instructor_id)
            )

            if instructor_query is None:
                abort(404)

        except:
            abort(404)

        instructor = instructor_query[0]

        try:
            # get request body
            body = request.get_json()

            if body is None:
                abort(400)

        except:
            abort(400)

        new_first_name = body.get("first_name", None)
        new_last_name = body.get("last_name", None)
        new_schedule = body.get("workdays", None)
        new_instruments = body.get("new_instruments", None)
        removed_instruments = body.get("removed_instruments", None)
        new_courses = body.get("new_courses", None)
        removed_courses = body.get("removed_courses", None)

        new_instruments_list = None
        new_courses_list = None
        removed_instruments_list = None
        removed_courses_list = None

        # update each piece of information if provided
        if new_first_name:
            instructor.first_name = new_first_name.title()

        if new_last_name:
            instructor.last_name = new_last_name.title()

        if new_schedule:
            instructor.schedule = format_schedule(new_schedule)

        if new_instruments:
            # check list of instruments, if provided, against database and create dict with names and ids
            new_instruments_list = check_instruments(new_instruments, instruments_dict)

        if new_instruments_list:
            # add rows to association table for each instrument in dict
            for instrument in new_instruments_list:
                instrument_join = InstructorInstrumentRelationship(
                    instructor_id=instructor_id, instrument_id=instruments_dict[instrument]
                )
                instrument_join.insert()

        if removed_instruments:
            # check list of instruments to be deassociated from instructor, if provided, against database and create dict with names and ids
            removed_instruments_list = check_instruments(
                removed_instruments, instruments_dict
            )

        if removed_instruments_list:
            # remove rows from association table for each instrument in dict
            for instrument in removed_instruments_list:
                instrument_join_query = db.session.execute(
                    db.select(InstructorInstrumentRelationship)
                    .where(InstructorInstrumentRelationship.instructor_id == instructor_id)
                    .where(
                        InstructorInstrumentRelationship.instrument_id
                        == instruments_dict[instrument]
                    )
                ).one_or_none()

                if instrument_join_query is None:
                    pass

                else:
                    instrument_join_query[0].delete()

        if new_courses:
            # check list of courses, if provided, against database and create dict with names and ids
            courses_dict = get_courses_dict()
            new_courses_list = check_courses(new_courses, courses_dict)

        if new_courses_list:
            # add rows to association table for each course in dict
            for course in new_courses_list:
                course_join = InstructorCourseRelationship(
                    instructor_id=instructor_id, course_id=courses_dict[course]
                )
                course_join.insert()

        if removed_courses:
            # check list of courses to be deassociated from instructor, if provided, against database and create dict with names and ids
            courses_dict = get_courses_dict()
            removed_courses_list = check_courses(removed_courses, courses_dict)

        if removed_courses_list:
            # remove rows from association table for each course in dict
            for course in removed_courses_list:
                course_join_query = db.session.execute(
                    db.select(InstructorCourseRelationship)
                    .where(InstructorCourseRelationship.instructor_id == instructor_id)
                    .where(InstructorCourseRelationship.course_id == courses_dict[course])
                ).one_or_none()

            if course_join_query is None:
                pass

            else:
                course_join_query[0].delete()

        if new_first_name or new_last_name or new_schedule:
            try:
                # update instructor in database
                instructor.update()

            except IntegrityError:
                # throw error for duplicate name
                raise BadInfoError(
                    {
                        "code": 422,
                        "description": "An instructor by that name already exists!",
                    },
                    422,
                )

        return jsonify({"success": True})


    @app.route("/courses/<int:course_id>", methods=["PATCH"])
    @requires_auth("patch:courses")
    def update_course(payload, course_id):
        # get course by provided id
        course_query = db.one_or_404(
            db.select(Course).where(Course.id == course_id)
        ).one_or_none()

        course = course_query[0]

        try:
            # get request body
            body = request.get_json()

            if body is None:
                abort(400)

        except:
            abort(400)

        new_title = body.get("title", None)
        new_schedule = body.get("schedule", None)
        new_instructors = body.get("new_instructors", None)
        removed_instructors = body.get("removed_instructors", None)

        new_instructors_list = None
        removed_instructors_list = None

        # update each piece of information if provided
        if new_title:
            course.name = new_title

        if new_schedule:
            course.schedule = format_schedule(new_schedule)

        if new_instructors:
            # check list of instructors, if provided, against database and create dict with names and ids
            new_instructors_list = check_instructors(new_instructors, instructors_dict)

        if new_instructors_list:
            # add rows to association table for each instructor in dict
            for instructor in new_instructors_list:
                instructor_join = InstructorCourseRelationship(
                    instructor_id=instructors_dict[instructor], course_id=course_id
                )
                instructor_join.insert()

        if removed_instructors:
            # check list of instructors to be deassociated from course, if provided, against database and create dict with names and ids
            removed_instructors_list = check_instructors(
                removed_instructors, instructors_dict
            )

        if removed_instructors_list:
            # delete rows from association table for each instructor in dict
            for instructor in removed_instructors_list:
                instructor_join_query = db.session.execute(
                    db.select(InstructorCourseRelationship)
                    .where(
                        InstructorCourseRelationship.instructor_id
                        == instructors_dict[instructor]
                    )
                    .where(InstructorCourseRelationship.course_id == course_id)
                ).one_or_none()

                if instructor_join_query is None:
                    pass

                else:
                    instructor_join_query[0].delete()

        if new_title or new_schedule:
            try:
                # update course in database
                course.update()

            except IntegrityError:
                # throw error for duplicate name
                raise BadInfoError(
                    {"code": 422, "description": "A course by that name already exists!"},
                    422,
                )

        return jsonify({"success": True})


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


    @app.errorhandler(AuthError)
    def auth_error(error):
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

    return app

### launch

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        app.debug = True
        app.run(host="0.0.0.0")
