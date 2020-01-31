from wtforms import Form, StringField, SelectField
from wtforms.validators import DataRequired
from wtforms import validators

class phosphositesSearchForm(Form):
    choices = [('Substrate', 'Substrate')]
    select = SelectField(choices=choices)
    search = StringField('',[validators.DataRequired()])

class inhibitorsSearchForm(Form):
    choices = [(' ChEMBL ID ', ' ChEMBL ID '), ('INN_Name', 'INN_Name')]
    select = SelectField(choices=choices)
    search = StringField('',[validators.DataRequired()])
