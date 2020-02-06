from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///KinaseDatabasev1.db'
app.config['secret_key'] = 'YouDontKnow'
# app.secret_key = '_Hdjghdgsdf495/'

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)