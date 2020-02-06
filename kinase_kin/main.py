from flask import Flask, render_template, flash, redirect, request, url_for

#from forms import FileRequired
import os

from werkzeug.utils import secure_filename
from wtforms import Form, StringField, SelectField, validators, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed

from db_creator import init_db, db_session
from models import KinaseInfo, SubstrateInfo, InhibitorInfo
from app import app


class FileForm(Form):
	file = FileField(validators=[FileRequired()])
	submit = SubmitField('Submit')
#NameError: name 'SubmitField' is not defined
##################################################################

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

# class phosphositesSearchForm(Form):
#     choices = [('Phosphosite', 'Phosphosite')]
#     select = SelectField(choices=choices)
#     search = StringField('',[validators.DataRequired()])
############################################################################################

init_db() #initialise the db

############################################################################################



############################  Home   #############################################################
@app.route('/', methods=['GET', 'POST'])
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

			inhibitor_qry = db_session.query(KinaseInfo, InhibitorInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(InhibitorInfo, KinaseInfo.Kinase_Symbol== InhibitorInfo.Kinase_Target) #run join query to find all inhibitors with the corresponding kinase symbol target
			inhibitor_results = inhibitor_qry.all()

			substrate_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
			substrate_results = substrate_qry.all()

		elif search.data['select'] == 'Uniprot Accession Number': #check Uniprot Accession Number search was selected
			Uniprot_qry =db_session.query(KinaseInfo).filter(KinaseInfo.Uniprot_Accession_Number.contains(search_string)) #qry uniprot accession number 
			Uniprot_results= Uniprot_qry.all()

	if not results:
		flash('No results found!') #flash error message
		return redirect('/Kinases') #return back to kinase search

	elif search.data['select'] == 'Uniprot Accession Number': # if user selected uniprot accession number
		return render_template('uniprot.html', Uniprot_results=Uniprot_results)

	else:
		return render_template('kinase_results.html', results=results, inhibitor_results=inhibitor_results, substrate_results=substrate_results)

@app.route('/Kinases/<Kinase_Symbol>')
def profile(Kinase_Symbol):
    qry = db_session.query(KinaseInfo).filter(KinaseInfo.Kinase_Symbol.ilike(Kinase_Symbol))
    results= qry.all()
    
    inhibitor_qry = db_session.query(KinaseInfo, InhibitorInfo)\
            .join(InhibitorInfo, KinaseInfo.Kinase_Symbol== InhibitorInfo.Kinase_Target)
    inhibitor_results = inhibitor_qry.all()
      
    substrate_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
    substrate_results = substrate_qry.all()
    
    return render_template('kinase_results.html', results=results, inhibitor_results = inhibitor_results, substrate_results = substrate_results)

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
def Data_Analysis():
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


############################  Inhibitors   ########################################################

@app.route('/Inhibitors', methods=['GET', 'POST'])
def Inhibitors():
	search = InhibitorSearchForm(request.form) #request search from & run request
	#may need to try submit as difference in forms
	if request.method== 'POST':
		return inhibitor_results(search)
	return	render_template('inhibitor_results.html', form=search)

@app.route('/Inhibitors_results')
def inhibitor_results(search):
	results = []
	search_string = search.data['search']

	if search_string:
		if search.data['select'] == 'CHEMBL ID':
			qry = db_session.query(InhibitorInfo).filter(InhibitorInfo.CHEMBLID.ilike(search_string))
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
		return render_template('inhibitor_results.html')

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
	return	render_template('Substrate_results.html', form=search)

@app.route('/Substrate_results')
def substrate_results(search):
	results= []
	search_string = search.data['search']

	if search_string:
		if search.data['select'] == 'Substrate':
			qry.db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.ilike(search))
			results = qry.all()
		else:
			qry = db_session.query(SubstrateInfo)
			results = qry.all()

	if not results:
		flash('No results found. Please search again')#
		return redirect('/Substrates')
	else:
		return render_template('substrate_results.html')

@app.route('/Substrates/<Substrate_Symbol>')
def substrateprofile(Substrate_Symbol):
	qry = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.ilike(Substrate_Symbols))
	results = qry.all()
	return render_template('Substrate_results.html', results = results)

######################################################################################################
if __name__=='__main__':
	app.run(debug=True)
	# from waitress import serve
	# serve(app, host="0.0.0.0", port=8080)
