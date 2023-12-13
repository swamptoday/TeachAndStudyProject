from unicodedata import name
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Curriculum, Note, User, Tutor
from . import db
import json



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
    return render_template("calendar.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Fetch the current user
        user = current_user
        
        # Update user data
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.address = request.form.get('address')

        # Commit changes to the database
        db.session.commit()

    return render_template("profile.html", user=current_user)

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

    return render_template("curriculum_add.html", user=current_user)

@views.route('/tutors', methods=['GET'])
def tutors():

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
    for tutor in new_tutors:
        print(tutor)
    return render_template("tutors.html", user=current_user, tutors=new_tutors)