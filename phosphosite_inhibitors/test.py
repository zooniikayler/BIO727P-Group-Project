
from flask import Flask, render_template, url_for, request, redirect
from forms import phosphositesSearchForm, inhibitorsSearchForm

app = Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template('Kinase_home_page.html')

@app.route('/inhibitors', methods=['GET', 'POST'])
def inhibitors():
    search = inhibitorsSearchForm(request.form)
    return render_template('inhibitors.html', form=search)

@app.route('/phosphosites', methods=['GET', 'POST'])
def phosphosites():
    search = phosphositesSearchForm(request.form)
    return render_template('phosphosites.html', form=search)

if __name__ == '__main__':
	app.run(debug=True)
