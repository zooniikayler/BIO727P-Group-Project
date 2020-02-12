from flask import Flask, render_template, flash, redirect, request, url_for, send_from_directory
from app import app
from analysis_pipe import *
import numpy as np
from db_creator import init_db, db_session
from models import KinaseInfo,SubstrateInfo,InhibitorInfo,InhibitorRef

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
	choices = [('Inhibitor International Nonproprietary Name (INN)', 'Inhibitor International Nonproprietary Name (INN)')] # Define choices for the kinase search
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
	if request.method== 'POST': #if user posting search string to get info from db
		return kinase_results(search) #Run kinase search function
	return	render_template('Kinases.html', form=search)


@app.route('/kinase_results')
def kinase_results(search):
	results = []
	search_string = search.data['search'] #when given user input data

	if search_string:
		if search.data['select']=='Kinase Name': #check if kinase symbol was selected
			qry = db_session.query(KinaseInfo).filter(KinaseInfo.Kinase_Symbol.ilike(search_string))
			results= qry.all() #output all query results

			inhib_qry = db_session.query(InhibitorRef, InhibitorInfo)\
					.filter(InhibitorRef.Kinase_Target.ilike(search_string))\
					.join(InhibitorInfo, InhibitorInfo.CHEMBLID == InhibitorRef.CHEMBL_ID) #run join query to find all inhibitors with the corresponding kinase symbol target
			inhibitor_results = inhib_qry.all()

			sub_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
			substrate_results = sub_qry.all()

		elif search.data['select'] == 'Uniprot Accession Number': #check Uniprot Accession Number search was selected
			qry =db_session.query(KinaseInfo).filter(KinaseInfo.Uniprot_Accession_Number.ilike(search_string)) #qry uniprot accession number 
			results= qry.all()

			inhib_qry = db_session.query(InhibitorRef, InhibitorInfo)\
					.filter(InhibitorRef.Kinase_Target.ilike(search_string))\
					.join(InhibitorInfo, InhibitorInfo.CHEMBLID == InhibitorRef.CHEMBL_ID) #run join query to find all inhibitors with the corresponding kinase symbol target
			inhibitor_results = inhib_qry.all()

			sub_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
			substrate_results = sub_qry.all()

		else:
			qry = db_session.query(KinaseInfo)
			results = qry.all()

	if not results:
		flash('No results found!', "error") #flash error message
		return redirect('/Kinases') #return back to kinase search


	else:
		return render_template('kinase_results.html', results=results, inhibitor_results=inhibitor_results, substrate_results=substrate_results)

@app.route('/Kinases/<Kinase_Symbol>')
def profile(Kinase_Symbol):
    qry = db_session.query(KinaseInfo).filter(KinaseInfo.Kinase_Symbol.ilike(Kinase_Symbol))
    results= qry.all()
    
    inhib_qry = db_session.query(KinaseInfo, InhibitorInfo)\
            .join(InhibitorRef, KinaseInfo.Kinase_Symbol== InhibitorRef.Kinase_Target)
    inhibitor_results = inhib_qry.all()
      
    sub_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
    substrate_results = sub_qry.all()
    
    return render_template('kinase_results.html', results=results, inhibitor_results = inhibitor_results, substrate_results = substrate_results)


############################  About us   #########################################################


@app.route('/About_us')
def About_us():
	return	render_template('About_us.html')

############################  Data Analysis   #########################################################


UPLOAD_FOLDER = 'cache'

ALLOWED_EXTENSIONS= {'csv', 'tsv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/Data_Analysis', methods = ['GET', 'POST'])
def Upload():
	form = FileForm()
	if request.method == 'POST':
		if request.files:
			file=request.files['file']
			if file.filename == '':
				flash('No file selected')
				return redirect(request.url)
			filename = secure_filename(file.filename)
			if file and allowed_file(file.filename):
				if not os.path.exists(UPLOAD_FOLDER):
					os.makedirs(UPLOAD_FOLDER)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				return redirect(url_for('results', filename = filename))
	return render_template('Data_Analysis.html', form=form)


@app.route('/data_results')
def results():
	print("getting results page")
	# passing uploaded file to the results function
	filename = request.args.get('filename')
	if get_format(os.path.join(app.config['UPLOAD_FOLDER'], filename)) == 1:
		return redirect(url_for('format_error'))
	print("hi")
	# creating/cleaning a dataframe from database and userdata
	df = create_df_user(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	x_axis = list(set(df.Kinase))  # getting unique set of kinases from uploaded file

	# calculating mean score for all values of y without using a for-loop
	y_value_mean = lambda y: mean_score(y, dataset=df)
	y_value_delta = lambda y: delta_score(0.05, y, dataset=df)
	y_axis_mean = [y_value_mean(x) for x in x_axis]
	y_axis_delta = [y_value_delta(x) for x in x_axis]

	list_obj = []  # creating dictionary of kinases/activity for mean score without kinases of score 0
	for a in range(len(x_axis)):
		obj = {
			"x": x_axis[a],
			"y": y_axis_mean[a],
		}
		if obj["y"] != 0:
			list_obj.append(obj)

	list_obj_delta = []  # creating dictionary of kinases/activity for delta score without kinases of score 0
	for a in range(len(x_axis)):
		obj = {
			"x": x_axis[a],
			"y": y_axis_delta[a],
		}
		if obj["y"] != 0:
			list_obj_delta.append(obj)

	# sorting lists of dictionary objects by key so they appear in ascending order
	sorted_list_mean = sorted(list_obj, key=lambda k: k['y'])
	sorted_list_delta = sorted(list_obj_delta, key=lambda k: k['y'])

	barplot_x = [item['x'] for item in sorted_list_mean]  # extracting x from dictionary
	barplot_y = [item['y'] for item in sorted_list_mean]  # extracting y from dictionary
	colours = [i for i in range(len(x_axis))]  # creating a color index for each kinase

	# getting bottom and top ten lists of greatest fold change
	tten_x1 = barplot_x[:10]
	tten_x2 = barplot_x[-10:]
	tten_y1 = barplot_y[:10]
	tten_y2 = barplot_y[-10:]

	# concatenating bottom and top ten lists of greatest fold change kinases
	tten_x = tten_x1 + tten_x2
	tten_y = tten_y1 + tten_y2

	delta_x = [item['x'] for item in sorted_list_delta]  # extracting x from dictionary
	delta_y = [item['y'] for item in sorted_list_delta]  # extracting y from dictionary

	# volcano plot
	volcano_x = list(df.FC_log2)  # extracting fold change data from the uploaded file
	volcano_y = list(df.pval5)  # extracting pvalues from the uploaded file
	volcano_range = max(volcano_y)
	labels = list(df.Kinase)

	return render_template("data_results.html", y_axis=barplot_y, x_axis=barplot_x, colours=colours,  volcano_x=volcano_x,
						volcano_y=volcano_y, tten_x=tten_x, tten_y=tten_y, delta_y=delta_y, delta_x=delta_x, labels=labels, y_range=volcano_range)


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
	inhibitor_results = []
	search_string = search.data['search']

	if search_string:
		if search.data['select'] == 'Inhibitor International Nonproprietary Name (INN)':
			qry = db_session.query(InhibitorInfo).filter(InhibitorInfo.Inhibitor_Name.contains(search_string))
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
			qry = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.contains(search_string))
			results = qry.all()
		else:
			qry = db_session.query(SubstrateInfo)
			results = qry.all()

	if not results:
		flash('No results found. Please search again')#
		return redirect('/Substrates')
	else:
		return render_template('substrate_results.html', results=results)



@app.route('/Substrates/<Substrate>')
def substrateprofile(Substrate):
	qry = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.ilike(Substrate))
	results = qry.all()
	#chromosome = qry.Chromosome()
	#source_url = 'http://genome-euro.ucsc.edu/cgi-bin/hgTracks?db=hg38&lastVirtModeType=default&lastVirtModeExtraState=&virtModeType=default&virtMode=0&nonVirtPosition=&position=chr' + chromosome + '%3A' + view1 + '%2D' + view2 + '&hgsid=235662278_hbN0IQVHHXUisaAA0FwbcsOHxqqQ'
	return render_template('Substrate_results.html', results = results)


@app.route('/genome_browser')
def genome_browser():
	return render_template('genome_browser.html')


######################################################################################################
if __name__=='__main__':
	app.run(debug=True)
	# from waitress import serve
	# serve(app, host="0.0.0.0", port=8080)
    
