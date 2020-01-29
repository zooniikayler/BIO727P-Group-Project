from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextField 
from wtforms.validators import Required, InputRequired, FileField, FileAllowed, FileRequired
from flask_wtf import Form
from wtforms import SelectField

# Create search forms for the three searches on the site

class KinaseSearchForm(Form):
	choices = [('Kinase Symbol', 'Kinase Symbol')] # Define choices for the kinase search
	search = StringField("Enter valid Kinase Name", choices=choices, validators=[InputRequired()]) #Search Field will include choices defined
	submit = SubmitField("Search", [validators.DataRequired()])


class InhibitorSearchForm(Form):
	choices = [(' CHEMBL_ID', 'CHEMBL_ID'), ('INN_Name', 'INN_Name')]
	search = Stringfield("Search for a Kinase Inhibitor", choices=choices, validators=[InputRequired()]) # Define choices for the inhibitor search
	submit = SubmitField("Search", [validators.DataRequired()])

class PhosphositeSearchForm(Form):
	choices = [('Substrate', 'Substrate')]# Define choices for the phosphosite search
    select = SelectField('Search for Substrate:', choices=choices)
    search = StringField('',[validators.DataRequired()])# this is a field that is empty that allows the user to search - a data required validator is added.

#class Data_Analysis(Form):
	#file = FileField("Upload File tp be analysed", validators=[InputRequired()])
	#submit = SubmitField("Search")

