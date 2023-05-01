### imports

from typing import List

from config import db
from sqlalchemy import Column, String, Integer, ForeignKey

from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import ARRAY

### models

# lists of weekday values
weekdays_short = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
weekdays_long = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# association tables
class InstructorCourseRelationship(db.Model):
    instructor_id = Column(ForeignKey('instructors.id'), primary_key=True)
    course_id = Column(ForeignKey('courses.id'), primary_key=True)
    instructor = relationship('Instructor', back_populates='courses')
    course = relationship('Course', back_populates='instructors') 

class InstructorInstrumentRelationship(db.Model):
    instructor_id = Column(ForeignKey('instructors.id'), primary_key=True)
    instrument_id = Column(ForeignKey('instruments.id'), primary_key=True)
    instructor = relationship('Instructor', back_populates='instruments')
    instrument = relationship('Instrument', back_populates='instructors')

# main models
class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    schedule = Column(ARRAY(String(length=3)), nullable=False)
    courses: Mapped[List['InstructorCourseRelationship']] = relationship(back_populates='instructor')
    instruments: Mapped[List['InstructorInstrumentRelationship']] = relationship(back_populates='instructor')


class Course(db.Model):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    schedule = Column(ARRAY(String(length=3)))
    instrument_id = Column(ForeignKey('instruments.id'), nullable=False)
    instrument = relationship('Instrument', back_populates='courses')
    instructors: Mapped[List['InstructorCourseRelationship']] = relationship(back_populates='course')
    

class Instrument(db.Model):
    __tablename__ = 'instruments'

    id = Column(Integer, primary_key=True)
    instrument = Column(String, nullable=False)
    instructors: Mapped[List['InstructorInstrumentRelationship']] = relationship(back_populates='instrument')
    courses = relationship('Course', back_populates='instrument')
