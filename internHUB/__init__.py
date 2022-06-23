from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

app = Flask(__name__)
import os
secret_key = os.urandom(16)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/felix/VSCODE/flask-web-app/internhub/internHUB/role.db'

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from internHUB import routes