from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10), unique=True)
    date_added = db.Column(db.DateTime(timezone=True), default = func.now())
    is_student = db.Column(db.Boolean)
    is_tutor = db.Column(db.Boolean)
    notes = db.relationship('Note')
    student = db.relationship('Student', uselist=False, back_populates='user')
    tutor = db.relationship('Tutor', uselist=False, back_populates='user')

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='student')
    calendars = db.relationship('Calendar')
    
class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    description = db.Column(db.String)
    subjects = db.Column(db.String)
    user = db.relationship('User', back_populates='tutor')
    curriculums = db.relationship('Curriculum')
    calendars = db.relationship('Calendar')

    
class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String)
    amount = db.Column(db.Integer)
    level = db.Column(db.String(50))
    topics = db.Column(db.String)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    
class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

#add description to tutor
#add subject to tutor