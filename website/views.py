from unicodedata import name
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Curriculum, Note, User, Tutor, Calendar, Student
from . import db
import json
from datetime import datetime


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/calendar', methods=['GET'])
@login_required
def calendar():
    if current_user.is_tutor:
        tutor = Tutor.query.filter_by(user_id = current_user.id).first()
        events = Calendar.query.filter_by(tutor_id = tutor.id).all()
        formatted_events = []
        for event in events:
            user = User.query.filter_by(id = event.student_id).first()
            formatted_event = {
                'id': f'{event.id}',  # Assuming you want the ID as a 6-digit string
                'name': 'Заняття',  # Replace this with the actual event name from your data
                'description': "У вас заняття з учнем " + user.first_name + " " + user.last_name +" :)",
                'date': event.date.strftime('%m/%d/%Y'),  # Format date as 'mm/dd/yyyy'
                'type': 'event'
            }
        formatted_events.append(formatted_event)
    elif current_user.is_student:
        student = Student.query.filter_by(user_id = current_user.id).first()
        events = Calendar.query.filter_by(student_id = student.id).all()
        formatted_events = []
        for event in events:
            print(event)
            user = User.query.filter_by(id = event.tutor_id).first()
            formatted_event = {
                'id': f'{event.id}',  # Assuming you want the ID as a 6-digit string
                'name': 'Заняття',  # Replace this with the actual event name from your data
                'description': "У вас заняття з репетитором " + user.first_name + " " + user.last_name +" :)",
                'date': event.date.strftime('%m/%d/%Y'),  # Format date as 'mm/dd/yyyy'
                'type': 'event'
            }
            formatted_events.append(formatted_event)
       
    
    return render_template("calendar.html", user=current_user, events=formatted_events)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    tutor = None

    if current_user.is_tutor == True:
        tutor = Tutor.query.filter_by(user_id = current_user.id).first()
    if request.method == 'POST':
        # Fetch the current user
        user = current_user
        
        # Update user data
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')
        
        if current_user.is_tutor == True:
            tutor.description = request.form.get('description')
            tutor.subjects = request.form.get('subjects')
            print(tutor.description)
            print(request.form.get('description'))
            db.session.commit()


        # Commit changes to the database
        db.session.commit()
        
        print(tutor.description)

    return render_template("profile.html", user=current_user, tutor = tutor)

@views.route('/curriculum', methods=['GET'])
@login_required
def curriculum():
    if current_user.is_student:
        flash("Сторінки не існує!", category='error')
        return redirect(url_for('views.home'))
        # Fetch the current user's ID
    current_user_id = current_user.id
    
    # Find the tutor entity with the same user ID as the current user
    tutor = Tutor.query.filter_by(user_id=current_user_id).first()
    if tutor:
        curriculums = Curriculum.query.filter_by(tutor_id=tutor.id).all()
    else:
        curriculums = []  # If no tutor found for the user, set curriculums to an empty list
    return render_template("curriculum.html", user=current_user, curriculums = curriculums)

@views.route('/curriculum/add', methods=['GET', 'POST'])
@login_required
def curriculum_add():
    if current_user.is_student:
        flash("Сторінки не існує!", category='error')
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            amount = request.form.get('amount')
            level = request.form.get('level')
            topics = request.form.get('topics')
            tutor_id = current_user.id
            print(name, description, amount, level, topics, tutor_id)
            new_curriculum = Curriculum(name=name, description=description, amount=amount, level=level, topics=topics, tutor_id=tutor_id)
            db.session.add(new_curriculum)
            db.session.commit()
            return redirect(url_for('views.curriculum'))

    return render_template("curriculum_add.html", user=current_user)

@views.route('/tutors', methods=['GET', 'POST'])
def tutors():
    if request.method == 'POST':
        date = request.form.get('date')
        formatted_date = datetime.fromisoformat(date)

        tutor_email = request.form.get('tutor')
        user_tutor = User.query.filter_by(email = tutor_email).first()
        tutor = Tutor.query.filter_by(user_id = user_tutor.id).first()
        student = Student.query.filter_by(user_id = current_user.id).first()
        new_calendar = Calendar(date=formatted_date, tutor_id = tutor.id, student_id = student.id)
        db.session.add(new_calendar)
        db.session.commit()
    # Fetch the current user's ID
    # Find the tutor entity with the same user ID as the current user
    tutors = Tutor.query.all()
    users = User.query.filter_by(is_tutor = True).all()
    # Create dictionaries to store counts
    tutor_counts = {}
    user_counts = {}

    # Store the counts without iterating
    for tutor in tutors:
        tutor_id = tutor.user_id
        if tutor_id not in tutor_counts:
            tutor_counts[tutor_id] = 0
        tutor_counts[tutor_id] += 1

    for user in users:
        user_id = user.id
        if user_id not in user_counts:
            user_counts[user_id] = 0
        user_counts[user_id] += 1

    # Create a new array with attributes from User model
    new_tutors = []
    for user in users:
        user_dict = user.__dict__.copy()  # Get the user attributes
        user_id = user_dict.pop('id')  # Remove 'id' to avoid duplication
        new_tutor_dict = {**user_dict, 'tutors': tutor_counts.get(user_id, 0), 'users': user_counts.get(user_id, 0)}
        new_tutors.append(new_tutor_dict)
    print(new_tutors)

    return render_template("tutors.html", user=current_user, tutors=new_tutors)