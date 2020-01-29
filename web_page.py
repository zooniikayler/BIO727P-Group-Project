from flask import Flask
kin_app = Flask(__name__)

@kin_app.route("/Home")
def home():
    return ""

@kin_app.route("/Upload Data")
def home():
    return "<h1>Upload your proteomics data<h1> File must " \
           " be formatted to have columns:[1] Substrates(Position) [2] control_mean " \
           "[3] condition_mean [4] FC [5] p_val [6] Any"

@kin_app.route("/Substrates")
def home():
    return "<h1>Upload your proteomics data<h1> File must " \
           " be formatted to have columns:[1] Substrates(Position) [2] control_mean " \
           "[3] condition_mean [4] FC [5] p_val [6] Any"

@kin_app.route("/Kinases")
def home():
    return "<h1>Upload your proteomics data<h1> File must " \
           " be formatted to have columns:[1] Substrates(Position) [2] control_mean " \
           "[3] condition_mean [4] FC [5] p_val [6] Any"

@kin_app.route("/Data Analysis")
def home():
    return "<h1>Upload your proteomics data<h1> File must " \
           " be formatted to have columns:[1] Substrates(Position) [2] control_mean " \
           "[3] condition_mean [4] FC [5] p_val [6] Any"

if __name__ == '__main__':
    kin_app.run(debug=True)
