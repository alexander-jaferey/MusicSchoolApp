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
            name = f"{instructor.first_name} {instructor.last_name[0]}"
            print(name)
            instruments_query = db.session.execute(db.select(Instrument).join(InstructorInstrumentRelationship).where(InstructorInstrumentRelationship.instructor_id == id))
            
            for instrument in instruments_query:
                instruments.append(instrument[0].instrument)

            info[name] = instruments
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

### launch

if __name__ == "__main__":
    with app.app_context():
        app.debug = True
        app.run()
