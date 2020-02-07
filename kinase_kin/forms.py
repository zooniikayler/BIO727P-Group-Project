# from flask_wtf import FlaskForm
# from wtforms import Form, StringField, SelectField, validators, SubmitField, FileField
# from wtforms.validators import DataRequired
# from flask_wtf.file import FileRequired, FileField, FileAllowed

# # Create search forms for the three searches on the site

# class KinaseSearchForm(Form):
# 	#choices = [('Kinase Symbol', 'Kinase Symbol')] # Define choices for the kinase search
# 	search = StringField('Enter a Kinase Name', validators=[DataRequired()]) #Search Field will include choices defined
# 	submit = SubmitField("Search")


# class InhibitorSearchForm(Form):
# 	#choices = [(' CHEMBL_ID', 'CHEMBL_ID'), ('INN_Name', 'INN_Name')]
# 	search = StringField('Enter a Kinase Inhibitor Name', validators=[DataRequired()]) # Define choices for the inhibitor search
# 	submit = SubmitField("Search")

# class SubstrateSearchForm(Form):
# 	#choices = [('Substrate', 'Substrate')]# Define choices for the phosphosite search
# 	search = StringField('Enter a Substrate', validators=[DataRequired()])
# 	submit = SubmitField('Search')

# class phosphositesSearchForm(Form):
#     choices = [('Phosphosite', 'Phosphosite')]
#     select = SelectField(choices=choices)
#     search = StringField('',[validators.DataRequired()])

# class FileForm(Form):
#     file = FileField(validators=[FileRequired()])
#     submit = SubmitField('Submit')

# #class Data_Analysis(Form):
# 	#file = FileField("Upload File tp be analysed", validators=[InputRequired()])
# 	#submit = SubmitField("Search")

