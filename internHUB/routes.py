from internHUB import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, url_for, flash
from internHUB.forms import *
from internHUB.models import *
import time
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index2.html')

# student signup
@app.route('/student_signup/', methods=['GET', 'POST'])
def student_signup():
    form = StudentRegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # create new user
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # create new student
        new_student = Student(username = form.username.data, student_id = new_user.id)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('student_login'))
    return render_template('student_signup.html', form=form)


# company signup
@app.route('/company_signup/', methods=['GET', 'POST'])
def company_signup():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        # create new user
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # create new company
        new_company = Company(company_name = form.company_name.data, company_id = new_user.id)
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('company_login'))
    return render_template('company_signup.html', form=form)


# student login
@app.route('/student_login/', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            student = Student.query.filter_by(username = form.username.data).first()
            if student and student.student_id == user.id:
                login_user(user)
                # flash('Successfully logged in')
                return redirect(url_for('student_dashboard'))
            # flash('Incorrect username')
        return redirect(url_for('student_login_form_error'))
    return render_template('student_login.html', form = form)

@app.route('/student_login_form_error')
def student_login_form_error():
    return render_template('student_login_form_error.html')

# company login
@app.route('/company_login/', methods=['GET', 'POST'])
def company_login():
    form = CompanyLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            company = Company.query.filter_by(company_name = form.company_name.data).first()
            if company and company.company_id == user.id:
                login_user(user) 
                # flash('Successfully logged in')
                return redirect(url_for('company_dashboard'))
            # flash('Incorrect username')
        return redirect(url_for('company_login_form_error'))
    return render_template('company_login.html', form = form)

@app.route('/company_login_form_error')
def company_login_form_error():
    return render_template('company_login_form_error.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    student = Student.query.filter_by(student_id = current_user.id).first()
    posts = CompanyCreatePost.query.all()
    company_names = []
    company_ids = []
    for post in posts:
        company = Company.query.filter_by(id = post.post_id).first()
        company_names.append(company.company_name)
        company_ids.append(company.id)
    if not student:
        logout_user(current_user)
        return redirect(url_for('student_login'))
    return render_template('student_dashboard.html', student = student, posts=posts, company_names=company_names, company_ids=company_ids)

@app.route('/company_dashboard/', methods=['GET', 'POST'])
@login_required
def company_dashboard():
    company = Company.query.filter_by(company_id=current_user.id).first()
    posts = CompanyCreatePost.query.filter_by(post_id = company.id).all()
    if not company:
        logout_user(current_user)
        return redirect(url_for('company_login'))
    return render_template('company_dashboard.html', company=company, posts = posts) 


@app.route('/company_create_post', methods=['GET', 'POST'])
@login_required
def company_create_post():
    form  = CompanyCreatePostForm()
    # print(current_user.id)
    if form.validate_on_submit():
        company = Company.query.filter_by(company_id=current_user.id).first()
        if company:
            new_post = CompanyCreatePost(title = form.title.data, description = form.description.data, post_id = company.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('company_create_post'))
    return render_template('company_create_post.html', form = form)

@app.route('/student_create_profile', methods=['GET', 'POST'])
@login_required
def student_create_profile():
    form = StudentCreateProfileForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(student_id=current_user.id).first()
        if student: 
            student_profile = StudentCreateProfile(school = form.school.data, course = form.course.data, year_of_study = form.year_of_study.data, skills = form.skills.data, profile_id = student.id)
            db.session.add(student_profile)
            db.session.commit()
            flash('Successfully created student profile')
            return redirect(url_for('student_create_profile'))
    return render_template('student_create_profile.html', form=form)

@app.route('/student_profile')
@login_required
def student_profile():
    student = Student.query.filter_by(student_id = current_user.id).first()
    profile = StudentCreateProfile.query.filter_by(profile_id = student.id).first()
    if not student:
        logout_user(current_user)
        return redirect(url_for('student_login'))
    return render_template('student_profile.html', student=student, profile=profile)

@app.route('/view_company/<int:company_id>', methods=['GET', 'POST'])
@login_required
def view_company(company_id):
    ###
    return redirect(url_for('company_profile'))

@app.route('/company_create_profile', methods=['GET', 'POST'])
@login_required
def company_create_profile():
    form = CompanyCreateProfileForm()
    if form.validate_on_submit():
        company = Company.query.filter_by(company_id = current_user.id).first()
        if company:
            company_profile = CompanyCreateProfile(domain = form.domain.data, location = form.location.data, description = form.description.data, profile_id = company.id)
            db.session.add(company_profile)
            db.session.commit()
            flash("Successfully created Company profile")
            return redirect(url_for('company_create_profile'))
    return render_template('company_create_profile.html', form = form)

@app.route('/company_profile')
@login_required
def company_profile():
    company = Company.query.filter_by(company_id = current_user.id).first()
    profile = CompanyCreateProfile.query.filter_by(profile_id = company.id).first()
    if not company:
        logout_user(current_user)
        return redirect(url_for('company_login'))
    return render_template('company_profile.html', company=company, profile=profile)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))