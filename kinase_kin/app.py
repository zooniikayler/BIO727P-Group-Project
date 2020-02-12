#Importing the required modules

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Setting up the Flask application
application= Flask(__name__)

#Setting up a connection to the database already created in memory
application.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///KinaseDatabasev1.db'

#setting up the secret key
application.config['secret_key'] = 'YouDontKnow'
application.secret_key = '_Hdjghdgsdf495/'

db = SQLAlchemy(application)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(application)