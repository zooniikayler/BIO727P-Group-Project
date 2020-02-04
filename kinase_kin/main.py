from flask import Flask, render_template, flash, redirect, request, url_for

#from forms import FileRequired
import os

from werkzeug.utils import secure_filename
from wtforms import Form, StringField, SelectField, validators, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed

from db_setup import init_db, db_session
from models import KinaseInfo, SubstrateInfo, InhibitorInfo


class FileForm(Form):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')

class KinaseSearchForm(Form):
	choices = [('Kinase Name', 'Kinase Name'), ('Uniprot Accession Number', 'Uniprot Accession Number')] # Define choices for the kinase search
	select = SelectField('Search for Kinase:', choices=choices) 
	search = StringField('',validators=[DataRequired()])


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
############################################################################################

init_db() #initialise the db

############################################################################################
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
	search = KinaseSearchForm(request.form) #request search from & run request
	#may need to try submit as difference in forms
	if request.method== 'POST': #if user posting search string to get info from db
		return kinase_results(search)
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
			qry =db_session.query(KinaseInfo).filter(KinaseInfo.Uniprot_Accession_Number.contains(search_string)) #qry uniprot accession number 
			results=qry.all()

	if not results:
		flash('No results found!') #flash error message
		return redirect('/Kinases') #return back to kinase search

	elif search.data['select'] == 'Uniprot Accession Number': # if user selected uniprot accession number
		return render_template('uniprot.html', results=results)
    
    else:
        #displaying results
        return render_template('kinase_results.html', results=results, inhibitor_results = inhibitor_results, substrate_results)

@app.route('/Kinases/<Kinase_Symbol>)
def profile(Kinase_Symbol):
    qry = db_session.query(KinaseInfo).filter(KinaseInfo.Kinase_Symbol.ilike(Kinase_Symbol))
    results= qry.all()
    
    inhibitor_qry = db_session.query(KinaseInfo, InhibitorInfo)\
            .join(InhibitorInfo, KinaseInfo.Kinase_Symbol== InhibitorInfo.Kinase_Target)
    inhibitor_results = inhibitor_qry.all()
      
    substrate_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
    substrate_results = substrate_qry.all()
    
    return render_template('kinase_results.html', results=results, inhibitor_results = inhibitor_results, substrate_results)

############################  About us   #########################################################

@app.route('/About_us')
def About_us():
	return	render_template('About_us.html')

############################  Data Analysis   #########################################################

# UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
# ALLOWED_EXTENSIONS= {'csv', 'tsv', 'txt'}

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/Data_Analysis', methods = ['GET', 'POST'])
# def Upload():
# 	form=FileForm()
# 	if request.method == 'POST':
# 		if request.files:
# 			file = request.files['file']
# 				#return redirect(request.url)
# 			#if file.filename == '':
# 				#flash('No file selected')
# 				#return redirect(request.url)
# 			if file and allowed_file(file.filename):

# 				upload_directory = os.path.join(app.instance_path, 'uploaded_file')
# 				if not os.path.exists(upload_directory):
# 					os.makedirs(upload_directory)
# 				file.save(os.path.join(upload_directory, secure_filename(file.filename)))
# 				return redirect(url_for('Home'))
# 	return	render_template('Data_Analysis.html', form=form)


# @app.route('/results', methods=['GET', 'POST'])
# def results():
# 	return render_template("results.html")




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
