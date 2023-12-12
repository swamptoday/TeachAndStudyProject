from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Student, Tutor
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('Неправильний пароль, спробуйте ще раз!.', category='error')
        else:
            flash('Користувача не існує!', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('first_name')
        lastName = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if (request.form.get('student_check') == 'student'):
            student_check = True
            tutor_check = False
        else: 
            student_check = False
            tutor_check = True                
        
        user = User.query.filter_by(email=email).first()
        if user: 
            flash('Email already exists.', category='error')
        elif len(email) < 4: 
            flash('Email must be greater than 3 characters.', category='error')
        elif (len(firstName) < 2 or len(lastName) < 2): 
            flash('First and last name must be greater than 1 character.', category='error')        
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')        
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=firstName,
                last_name=lastName,
                password=generate_password_hash(password1),
                is_student=student_check,
                is_tutor=tutor_check
            )
            db.session.add(new_user)
            db.session.commit()

            if student_check:
                user = User.query.filter_by(email=email).first()
                new_student = Student(user_id=user.id)
                print(user.id)
                print(new_student)
                db.session.add(new_student)
            else:
                user = User.query.filter_by(email=email).first()
                new_tutor = Tutor(user_id=user.id)
                print(user)
                print(new_tutor)
                db.session.add(new_tutor)

            db.session.commit()

            login_user(new_user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)