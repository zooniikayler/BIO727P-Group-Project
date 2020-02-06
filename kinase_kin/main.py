from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory

from kinase_kin.analysis_pipe import *
import numpy as np

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


UPLOAD_FOLDER = ('/Users/zooniikayler/PycharmProjects/BIO727P-Group-Project/kinase_kin/Data_Upload' )

ALLOWED_EXTENSIONS= {'csv', 'tsv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/Data_Analysis', methods = ['GET', 'POST'])
def Upload():
	form=FileForm()
	if request.method == 'POST':
		if request.files:
			file=request.files['file']
			if file.filename == '':
				flash('No file selected')
				return redirect(request.url)
			filename = secure_filename(file.filename)
			#filename = np.random()
			if file and allowed_file(file.filename):
				if not os.path.exists(UPLOAD_FOLDER):
					os.makedirs(UPLOAD_FOLDER)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return redirect(url_for('results', filename = filename))
	return render_template('Data_Analysis.html', form=form)



@app.route('/data_results')
def results():
	filename = request.args.get('filename')
	df= create_df_user(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	x_axis = list(set(df.Kinase))  # getting unique set of kinases from uploaded file
	y_axis = kinase_barplot_x(df)  # getting mean score for each kinase

	list_obj = []  # creating dictionary of kinases/activity
	for a in range(len(x_axis)):
		obj = {
			"x": x_axis[a],
			"y": y_axis[a],
		}
		list_obj.append(obj)

	sorted_list = sorted(list_obj, key=lambda k: k[
		'y'])  # sorting dictionary of kinases/activity so they appear in ascending order

	volcano_y = list(df.FC4)  # extracting fold change data from the uploaded file
	volcano_x = list(df.pval5)  # extracting pvalues from the uploaded file

	barplot_x = [item['x'] for item in sorted_list]  # extracting x from dictionary
	barplot_y = [item['y'] for item in sorted_list]  # extracting y from dictionary
	colours = [i for i in range(len(x_axis))]  # creating a color index for each kinase
	return render_template("data_results.html", y_axis=barplot_y, x_axis=barplot_x, colours = colours,  volcano_x=volcano_x, volcano_y = volcano_y)

#arguments are passing the variables from python for use in html script


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
