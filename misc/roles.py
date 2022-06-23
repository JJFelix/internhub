from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

app = Flask(__name__)

import os
secret_key = os.urandom(16)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/felix/VSCODE/flask-web-app/internhub/role.db'

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

#Models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    # company details
    
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer(), db.ForeignKey('users.id'), unique=True)
    company_name = db.Column(db.String(50), unique=True)
    location = db.Column(db.String(50))
    domain = db.Column(db.String(100))


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), unique=True)
    username = db.Column(db.String(15), unique = True)
    school_name = db.Column(db.String(100), unique = True)
    course = db.Column(db.String(100))

class CompanyCreatePost(db.Model):
    __tablename__ = 'company_posts'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('company.id'), unique=False)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Student Forms
class StudentRegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    school_name = StringField('school_name', validators=[InputRequired(), Length(min=1, max=100)])
    course = StringField('course', validators=[InputRequired(), Length(min=1)])
    password  =PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class StudentLoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email= StringField('email', validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# Company Forms
class CompanyRegisterForm(FlaskForm):
    company_name = StringField('company_name', validators=[InputRequired(), Length(min=4, max=50)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    location = StringField('location', validators=[InputRequired(), Length(min=1)])
    domain = StringField('domain', validators=[InputRequired(), Length(min=1)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class CompanyLoginForm(FlaskForm):
    company_name= StringField('company_name', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=8, max=80)])

class CompanyCreatePostForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max = 100)])
    description = StringField('description', validators=[InputRequired(), Length(min=1)])


# Routes
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
        new_student = Student(username = form.username.data, school_name = form.school_name.data , course = form.course.data, student_id = new_user.id)
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
        new_company = Company(company_name = form.company_name.data, location = form.location.data , domain = form.domain.data, company_id = new_user.id)
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
                return redirect(url_for('student_dashboard'))
            flash('Incorrect username')
        return redirect(url_for('student_login_form_error'))
    return render_template('student_login.html', form = form)

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
                return redirect(url_for('company_dashboard'))
            flash('Incorrect username')
        return redirect(url_for('company_login_form_error'))
    return render_template('company_login.html', form = form)


@app.route('/student_login_form_error')
def student_login_form_error():
    return render_template('student_login_form_error.html')

@app.route('/company_login_form_error')
def company_login_form_error():
    return render_template('company_login_form_error.html')

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    student = Student.query.filter_by(student_id = current_user.id).first()
    company = Company.query.filter_by(company_id=current_user.id).first()
    posts = CompanyCreatePost.query.filter_by(post_id = company.id).all()
    if not student:
        logout_user(current_user)
        return redirect(url_for('student_login'))
    return render_template('student_dashboard.html', student = student, posts=posts)

@app.route('/company_dashboard/', methods=['GET', 'POST'])
@login_required
def company_dashboard():
    company = Company.query.filter_by(company_id=current_user.id).first()
    posts = CompanyCreatePost.query.filter_by(post_id = company.id).all()
    if not company:
        logout_user(current_user)
        return redirect(url_for('company_login'))
    return render_template('company_dashboard.html', company=company, posts = posts) 


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/company_create_post', methods=['GET', 'POST'])
@login_required
def company_create_post():
    form  = CompanyCreatePostForm()
    print(current_user.id)
    if form.validate_on_submit():
        company = Company.query.filter_by(company_id=current_user.id).first()
        if company:
            new_post = CompanyCreatePost(title = form.title.data, description = form.description.data, post_id = company.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Successfully created new post')
            return redirect(url_for('company_create_post'))
    return render_template('company_create_post.html', form = form)

# @app.route('/test')
# @login_required
# def test():
#     form =  CompanyCreatePostForm()
#     company = Company.query.filter_by(company_id = current_user.id).first()
#     posts = CompanyCreatePost.query.filter_by(post_id = company.id).all()
#     return render_template('test.html', posts = posts)

if __name__ == '__main__': 
    app.run(debug=True)


