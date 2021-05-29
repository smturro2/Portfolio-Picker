from flask import Flask, render_template

app = Flask(__name__)


# Default home page - New Portfolio Page
# This page lets the user input a new portfolio.
@app.route('/')
@app.route('/NewPort')
def NewPort_Page():
    return render_template("NewPort.html")

# Strategy Page.
# This page allows you to find the best strategy given the risk amount.
@app.route('/Strategy')
def Strategy_Page():
    return render_template("Strategy.html")

# More Page.
# This page includes details about the project such as the written submissions.
@app.route('/More')
def More_Page():
    return render_template("More.html")


if __name__ == "__main__":
    app.run(debug=True)
