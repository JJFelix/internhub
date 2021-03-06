from internHUB import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer(), db.ForeignKey('users.id'), unique=True)
    company_name = db.Column(db.String(50), unique=True)

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('users.id'), unique=True)
    username = db.Column(db.String(15), unique = True)

class StudentCreateProfile(db.Model):
    __tablename__ = 'student_profile'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer(), db.ForeignKey('studentsde.id'), unique=True)
    school = db.Column(db.String(100))
    course = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer())
    skills = db.Column(db.String(500))
    # profile_picture = db.Column(db.String(100))

class CompanyCreatePost(db.Model):
    __tablename__ = 'company_posts'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('company.id'), unique=False)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))

class CompanyCreateProfile(db.Model):
    __tablename__ = 'company_profile'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer(), db.ForeignKey('company.id'), unique=True)
    domain = db.Column(db.String(50))
    location = db.Column(db.String(50))
    description = db.Column(db.String(500))
    # profile_picture = db.Column(db.String(100))


