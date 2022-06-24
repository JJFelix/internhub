from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length

class StudentRegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password  =PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class StudentLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email= StringField('Email', validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class StudentCreateProfileForm(FlaskForm):
    school = StringField('School', validators=[InputRequired(), Length(min=1)])
    course = StringField('Course', validators=[InputRequired(), Length(min=1)])
    year_of_study = IntegerField('Year of Study', validators=[InputRequired()])
    skills = StringField('Skills', validators=[InputRequired(), Length(min=1)])
    # profile_picture = StringField('profile_picture')


# Company Forms
class CompanyRegisterForm(FlaskForm):
    company_name = StringField('Company Name', validators=[InputRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class CompanyLoginForm(FlaskForm):
    company_name= StringField('Company Name', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=8, max=80)])

class CompanyCreatePostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(min=1, max = 100)])
    description = StringField('Description', validators=[InputRequired(), Length(min=1)])

class CompanyCreateProfileForm(FlaskForm):
    domain = StringField('Domain', validators=[InputRequired(), Length(min=1)])
    location = StringField('Location', validators=[InputRequired(), Length(min=1)])
    description  =StringField('Description', validators=[InputRequired(), Length(min=1)])
    # profile_picture = StringField('profile_picture')
