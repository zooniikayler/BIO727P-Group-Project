from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextField 
from wtforms.validators import Required, InputRequired
from flask_wtf import Form
from wtforms import SelectField

app = Flask(__name__)

app.config['SECRET_KEY'] = "DontTellAnyone"

##################### Index Page ################################
@app.route('/', methods=['GET', 'POST'])
@app.route('/Home')
def Home():
	return render_template('Home.html')

#####################  Kinases   #######################
@app.route('/Kinases')

class KinaseSearchForm(Form):
	choices = [('Kinase Symbol', 'Kinase Symbol')] # Define choices for the kinase search
	search = StringField("Enter valid Kinase Name", choices=choices, validators=[InputRequired()]) #Search Field will include choices defined
	submit = SubmitField("Search", [validators.DataRequired()])

def Kinases():
	form = KinaseSearchForm()
	if form.validate_on_submit():
		return 'Form Successfully Submitted'
	return	render_template('Kinases.html', form=form)

#####################  About us  #######################

@app.route('/About_us')
def About_us():
	return	render_template('About_us.html')

@app.route('/Data_Analysis')
def Data_Analysis():
	return	render_template('Data_Analysis.html')

@app.route('/Inhibitors')
def Inhibitors():
	return	render_template('Inhibitors.html')

@app.route('/Phosphosites')
def Phosphosites():
	return	render_template('Phosphosites.html')


if __name__=='__main__':
	app.run(degub=True)