from flask import Flask, render_template, flash, redirect, request, url_for

#from forms import FileRequired
import os
from werkzeug.utils import secure_filename
from wtforms import Form, StringField, SelectField, validators, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed


class FileForm(Form):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')

class KinaseSearchForm(Form):
	#choices = [('Kinase Symbol', 'Kinase Symbol')] # Define choices for the kinase search
	search = StringField('Enter a Kinase Name', validators=[DataRequired()]) #Search Field will include choices defined
	submit = SubmitField("Search")


class InhibitorSearchForm(Form):
	#choices = [(' CHEMBL_ID', 'CHEMBL_ID'), ('INN_Name', 'INN_Name')]
	search = StringField('Enter a Kinase Inhibitor Name', validators=[DataRequired()]) # Define choices for the inhibitor search
	submit = SubmitField("Search")

class SubstrateSearchForm(Form):
	#choices = [('Substrate', 'Substrate')]# Define choices for the phosphosite search
	search = StringField('Enter a Substrate', validators=[DataRequired()])
	submit = SubmitField('Search')

class phosphositesSearchForm(Form):
    choices = [('Phosphosite', 'Phosphosite')]
    select = SelectField(choices=choices)
    search = StringField('',[validators.DataRequired()])

#instantiate flask app
app = Flask(__name__)

#instantiate sqlalchemy objects
app.config['SECRET_KEY'] = "DontTellAnyone"


############################  Home   #############################################################

@app.route('/', methods=['GET', 'POST'])
@app.route('/Home')
def Home():
	return render_template('Home.html')

############################  Kinases   ##########################################################

@app.route('/Kinases', methods=['GET', 'POST'])
def Kinases():
	form = KinaseSearchForm()
	if form.validate():
		return 'Form Successfully Submitted'
	return	render_template('Kinases.html', form=form)

############################  About us   #########################################################

@app.route('/About_us')
def About_us():
	return	render_template('About_us.html')

############################  Data Analysis   #########################################################

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS= {'csv', 'tsv', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/Data_Analysis', methods = ['GET', 'POST'])
def Upload():
	form=FileForm()
	if request.method == 'POST':
		if request.files:
			file = request.files['file']
				#return redirect(request.url)
			#if file.filename == '':
				#flash('No file selected')
				#return redirect(request.url)
			if file and allowed_file(file.filename):

				upload_directory = os.path.join(app.instance_path, 'uploaded_file')
				if not os.path.exists(upload_directory):
					os.makedirs(upload_directory)
				file.save(os.path.join(upload_directory, secure_filename(file.filename)))
				return redirect(url_for('Home'))
	return	render_template('Data_Analysis.html', form=form)


@app.route('/results', methods=['GET', 'POST'])
def results():
	return render_template("results.html")




#@app.route('/Upload/Save/Analysis', methods=['POST'])


############################  Inhibitors   ########################################################

@app.route('/Inhibitors', methods=['GET', 'POST'])
def Inhibitors():
	form = InhibitorSearchForm()
	if form.validate():
		return 'Form Successfully Submitted'
	return	render_template('Inhibitors.html', form=form)

############################  Substrates   ########################################################
@app.route('/Substrates', methods=['GET', 'POST'])
def Substrates():
	form = SubstrateSearchForm()
	if form.validate():
		return 'Form Succesfully Submitted'
	return	render_template('Substrates.html', form=form)



if __name__=='__main__':
	app.run(debug=True)
	# from waitress import serve
	# serve(app, host="0.0.0.0", port=8080)
