from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class StudentRegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password  =PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class StudentLoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email= StringField('email', validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# Company Forms
class CompanyRegisterForm(FlaskForm):
    company_name = StringField('company_name', validators=[InputRequired(), Length(min=4, max=50)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class CompanyLoginForm(FlaskForm):
    company_name= StringField('company_name', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=8, max=80)])

class CompanyCreatePostForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max = 100)])
    description = StringField('description', validators=[InputRequired(), Length(min=1)])

