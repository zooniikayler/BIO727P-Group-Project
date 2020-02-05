from flask import Flask, render_template, flash, redirect, request, url_for
from .analysis_pipe import *


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
	choices = [(' CHEMBL ID', 'CHEMBL ID'), ('Inhibitor Name', 'Inhibitor Name')]
	select = StringField('Enter a Kinase Inhibitor Name', choices=choices) # Define choices for the inhibitor search
	search = StringField('',validators=[DataRequired()])

class SubstrateSearchForm(Form):
	choices = [('Substrate', 'Substrate')]# Define choices for the phosphosite search
	select = StringField('Enter Substrate Name', choices=choices) # Define choices for the inhibitor search
	search = StringField('',validators=[DataRequired()])

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
					.join(InhibitorInfo, KinaseInfo.Kinase_Symbol == InhibitorInfo.Kinase_Target) #run join query to find all inhibitors with the corresponding kinase symbol target
			inhibitor_results = inhibitor_qry.all()

			substrate_qry = db_session.query(KinaseInfo, SubstrateInfo)\
					.filter(KinaseInfo.Kinase_Symbol.ilike(search_string))\
					.join(SubstrateInfo, KinaseInfo.Kinase_Symbol == SubstrateInfo.Kinase)
			substrate_results = substrate_qry.all()

		elif search.data['select'] == 'Uniprot Accession Number': #check Uniprot Accession Number search was selected
			qry =db_session.query(KinaseInfo).filter(KinaseInfo.Uniprot_Accession_Number.contains(search_string)) #qry uniprot accession number 
			results=qry.all()

	if not results:
		flash('No results found. Please search again') #flash error message
		return redirect('/Kinases') #return back to kinase search

	elif search.data['select'] == 'Uniprot Accession Number': # if user selected uniprot accession number
		return render_template('uniprot.html', results=results)
    else:
        #displaying results
        return render_template('kinase_results.html', results=results, inhibitor_results = inhibitor_results, substrate_results)

@app.route('/Kinases/<Kinase_Symbol>)
def kinprofile(Kinase_Symbol):
    
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
ALLOWED_EXTENSIONS= {'csv'}

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
				upload_directory = os.path.join(app.instance_path)
				if not os.path.exists(upload_directory):
					os.makedirs(upload_directory)
				file.save(os.path.join(upload_directory, secure_filename(file.filename)))
				return redirect(url_for('results'))
	return	render_template('Data_Analysis.html', form=form)


@app.route('/results')
def results():
	y_axis = set(create_df_user('instance/sample_file.csv').Kinase)
	x_axis = kinase_barplot_x(create_df_user('instance/sample_file.csv'))
	barplot_dict = dict(y_axis, x_axis)

	return render_template("results.html")


############################  Inhibitors   ########################################################

@app.route('/Inhibitors', methods=['GET', 'POST'])
def Inhibitors():
    search = InhibitorSearchForm(request.form) #request search from & run request
	#may need to try submit as difference in forms
	if request.method== 'POST': #if user posting search string to get info from db
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
        return redirect ('/Inhibitors)
    else:
        return render_template('inhibitor_results.html')

@app.route('/Inhibitors/<chEMBL_ID>')
def inhibitorprofile(chEMBL_ID):
    qry = db_session.query(InhibitorInfo).filter(InhibitorInfo.CHEMBLID.ilike(chEMBL_ID))
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
        return render_template('substrate_results.html)

@app.route('/Substrates/<sub>)
def substrateprofile(sub):
    qry = db_session.query(SubstrateInfo).filter(SubstrateInfo.Substrate_Symbol.ilike(sub))
    results = qry.all()
    return render_template('Substrate_results.html', results = results)

############################################################################
if __name__=='__main__':
	app.run(debug=True)
	# from waitress import serve
	# serve(app, host="0.0.0.0", port=8080)
