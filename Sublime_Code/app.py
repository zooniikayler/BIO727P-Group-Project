from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#instantiate flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' # config db and sort relative path

db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)