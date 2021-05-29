from flask import Flask, render_template
import Gen_Stock_Data
from Portfolio_Manager import PortfolioManager


app = Flask(__name__)

port_manager = PortfolioManager()


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
    # Generate Fake Stock Data on site startup
    # todo: uncomment this
    # Gen_Stock_Data.run()

    # Run Website
    app.run(debug=True)
