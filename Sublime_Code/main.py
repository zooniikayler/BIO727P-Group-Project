import os
from flask import Flask, render_template, request, url_for
from forms import KinaseSearchForm, SubstrateSearchForm, InhibitorSearchForm


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

@app.route('/Data_Analysis')
def Data_Analysis():
	return	render_template('Data_Analysis.html')

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

@app.route('/Phosphosites')
def Phosphosites():
	form = phosphositesSearchForm()
	if form.validate():
		return "Form Successfully Submitted "
	return	render_template('phosphosites.html')



if __name__=='__main__':
	app.run(debug=True)
	# from waitress import serve
	# serve(app, host="0.0.0.0", port=8080)
