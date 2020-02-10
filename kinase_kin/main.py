from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory
from kinase_kin.app import app
from kinase_kin.analysis_pipe import *
import numpy as np
from kinase_kin.db_creator import init_db, db_session
from kinase_kin.models import KinaseInfo,SubstrateInfo,InhibitorInfo,InhibitorRef

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
	choices = [('Kinase Name', 'Kinase Name'), ('Uniprot Accession Number', 'Uniprot Accession Number')] # Define choices for the kinase search
	select = SelectField('Search for Kinase:', choices=choices) 
	search = StringField('Search',validators=[DataRequired()])


class InhibitorSearchForm(Form):
	choices = [('Inhibitor Name', 'Inhibitor Name'), ('ChEMBL ID', 'ChEMBL ID')] # Define choices for the kinase search
	select = SelectField('Search for Inhibitor:', choices=choices) 
	search = StringField('Search',validators=[DataRequired()])

class SubstrateSearchForm(Form):
	choices = [('Substrate', 'Substrate')] # Define choices for the kinase search
	select = SelectField('Search for Substrate:', choices=choices) 
	search = StringField('Search',validators=[DataRequired()])

############################################################################################

init_db() #initialise the db


############################  Home   #############################################################

@app.route('/')
@app.route('/Home')
def Home():
	return render_template('Home.html')

############################  Kinases   ##########################################################

@app.route('/Kinases', methods=['GET', 'POST'])
def Kinases():
	search = KinaseSearchForm(request.form) #request search from & run request
	#may need to try submit as difference in forms
	if request.method== 'POST': #if user posting search string to get info from db
		return kinase_results(search) #Run kinase search function
	return	render_template('Kinases.html', form=search)


@app.route('/kinase_results')
def kinase_results(search):
	results = []
	search_string = search.data['search'] #when given user input data
	#search_string = search_string.upper()

	if search_string:
		if search.data['select']=='Kinase Name': #check if kinase symbol was selected
			qry = db_session.query(KinaseInfo).filter(KinaseInfo.Kinase_Symbol.ilike(search_string))
			results= qry.all() #output all query results

			inhib_qry = db_session.query(InhibitorRef, InhibitorInfo)\
					.filter(InhibitorRef.Kinase_Target.ilike(search_string))\
					.join(InhibitorInfo, InhibitorInfo.CHEMBLID == InhibitorRef.CHEMBL_ID) #run join query to find all inhibitors with the corresponding kinase symbol target
			inhib_results = inhib_qry.all()

			sub_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
			sub_results = sub_qry.all()

		elif search.data['select'] == 'Uniprot Accession Number': #check Uniprot Accession Number search was selected
			qry =db_session.query(KinaseInfo).filter(KinaseInfo.Uniprot_Accession_Number.ilike(search_string)) #qry uniprot accession number 
			results= qry.all()

			inhib_qry = db_session.query(InhibitorRef, InhibitorInfo)\
					.filter(InhibitorRef.Kinase_Target.ilike(search_string))\
					.join(InhibitorInfo, InhibitorInfo.CHEMBLID == InhibitorRef.CHEMBL_ID) #run join query to find all inhibitors with the corresponding kinase symbol target
			inhib_results = inhib_qry.all()

			sub_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
			sub_results = sub_qry.all()

		else:
			qry = db_session.query(KinaseInfo)
			results = qry.all()

	if not results:
		flash('No results found!') #flash error message
		return redirect('/Kinases') #return back to kinase search


	else:
		return render_template('kinase_results.html', results=results, inhib_results=inhib_results, sub_results=sub_results)

@app.route('/Kinases/<Kinase_Symbol>')
def profile(Kinase_Symbol):
    qry = db_session.query(KinaseInfo).filter(KinaseInfo.Kinase_Symbol.ilike(Kinase_Symbol))
    results= qry.all()
    
    inhib_qry = db_session.query(KinaseInfo, InhibitorInfo)\
            .join(InhibitorRef, KinaseInfo.Kinase_Symbol== InhibitorRef.Kinase_Target)
    inhib_results = inhib_qry.all()
      
    sub_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
    sub_results = subs_qry.all()
    
    return render_template('kinase_results.html', results=results, inhib_results = inhib_results, sub_results = sub_results)


############################  About us   #########################################################


@app.route('/About_us')
def About_us():
	return	render_template('About_us.html')

############################  Data Analysis   #########################################################


UPLOAD_FOLDER = '/Users/zooniikayler/PycharmProjects/BIO727P-Group-Project/kinase_kin/Data_Upload'

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
	if check_format(os.path.join(app.config['UPLOAD_FOLDER'], filename)) == 1:
		return redirect(url_for('format_error'))

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

############################  Error Message   ########################################################


@app.route('/error-message')
def format_error():
	render_template("format_error.html")


############################  Inhibitors   ########################################################

@app.route('/Inhibitors', methods=['GET', 'POST'])
def Inhibitors():
	search = InhibitorSearchForm(request.form) 
	if request.method== 'POST':
		return inhibitor_results(search) #return inhibitor search function
	return	render_template('Inhibitors.html', form=search)

@app.route('/Inhibitors_results')
def inhibitor_results(search):
	results = []
	search_string = search.data['search']

	if search_string:
		if search.data['select'] == 'CHEMBL ID':
			qry = db_session.query(InhibitorInfo).filter(InhibitorInfo.CHEMBLID.ilike(search_string))
			# .join(InhibitorInfo,InhibitorInfo.CHEMBLID == InhibitorRef.CHEMBL_ID)
			results = qry.all()

		elif search.data['select'] == 'Inhibitor Name':
			qry = db_session.query(InhibitorInfo).filter(InhibitorInfo.Inhibitor_Name.ilike(search_string))
			results = qry.all()
		else:
			qry = db_session.query(InhibitorInfo)
			results = qry.all()

	if not results:
		flash('No results found. Please search again')
		return redirect ('/Inhibitors')

	else:
		return render_template('inhibitor_results.html', results=results)

@app.route('/Inhibitors/<Inhibitor_Name>')
def inhibitorprofile(Inhibitor_Name):
	qry = db_session.query(InhibitorInfo).filter(InhibitorInfo.Inhibitor_Name.ilike(Inhibitor_Name))
	results = qry.all()
	return render_template('inhibitor_results.html', results=results)

############################  Substrates   ########################################################
@app.route('/Substrates', methods=['GET', 'POST'])
def Substrates():
	search = SubstrateSearchForm(request.form) #request search from & run request
	#may need to try submit as difference in forms
	if request.method== 'POST': #if user posting search string to get info from db
		return substrate_results(search)
	return	render_template('Substrates.html', form=search)

@app.route('/Substrate_results')
def substrate_results(search):
	results= []
	search_string = search.data['search']

	if search_string:
		if search.data['select'] == 'Substrate':
			qry = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.contains(search))
			results = qry.all()
		else:
			qry = db_session.query(SubstrateInfo)
			results = qry.all()

	if not results:
		flash('No results found. Please search again')#
		return redirect('/Substrates')
	else:
		return render_template('substrate_results.html', results=results)


	# sub_obj = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.ilike(search)).first()

	# if sub_obj:
	# 	results['Substrate_Name'] = sub_obj.Substrate_Symbol
	# return render_template('substrate_results.html', results=results)


@app.route('/Substrates/<Substrate>')
def substrateprofile(Substrate):
	qry = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.ilike(Substrate))
	results = qry.all()

	return render_template('Substrate_results.html', results = results)

######################################################################################################
if __name__=='__main__':
	app.run(debug=True)
	# from waitress import serve
	# serve(app, host="0.0.0.0", port=8080)
    
