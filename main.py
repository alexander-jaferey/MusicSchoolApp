### imports

from flask_migrate import Migrate

from config import app, db
from models import Instructor, Course, Instrument, InstructorCourseRelationship, InstructorInstrumentRelationship

### app config

migrate = Migrate(app, db)

### controllers


@app.route("/")
def test():
    return "all is working"


### launch

if __name__ == "__main__":
    with app.app_context():
        app.debug = True
        app.run()
