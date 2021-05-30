from flask import Flask, render_template,request
import Gen_Stock_Data
from Portfolio_Manager import PortfolioManager
from Find_Best_Strategy import getBestStrategy, buildStrategyHTML
import pandas as pd
import numpy as np

app = Flask(__name__)

port_manager = PortfolioManager()


# Default home page - New Portfolio Page
# This page lets the user input a new portfolio.
@app.route('/')
@app.route('/NewPort')
@app.route('/NewPort', methods=['POST'])
def NewPort_Page():
    # Indicate if the user has submitted a portfolio
    submitted = False
    # Create a new portfolio is one was just submitted
    if request.method == 'POST':
        rowNum = 0
        list_ticker = list()
        list_weight = list()
        portName = request.values.get('portName')
        while True:
            ticker = request.values.get('stock_tick_'+str(rowNum))
            weight = request.values.get('stock_weight_'+str(rowNum))
            if(ticker != ""):
                list_ticker.append(ticker)
                if(weight == ""):
                    weight=1
                list_weight.append(weight)
                rowNum +=1
            else:
                break
        if (portName == ""):
            portName = "Portfolio " + str(port_manager.numPortfolios+1)
        port_manager.addPortfolio(list_ticker,list_weight,portName)
        submitted = True

    # Get the stock info dataframe
    df_stocks = pd.read_csv("DataFiles/StockInfo.csv")
    stocks_tickers = np.array(df_stocks['Symbol'])
    stocks_names = np.array(df_stocks['Security'])
    return render_template("NewPort.html",
                           tickers=stocks_tickers,
                           names=stocks_names,
                           indexes=np.arange(len(stocks_names)),
                           numPorts=port_manager.numPortfolios+1,
                           submittedAPort=submitted)

# Strategy Page.
# This page allows you to find the best strategy given the risk amount.
@app.route('/Strategy')
def Strategy_Page():
    return render_template("Strategy.html",outPut=False)


# Strategy Page output
# This page displays the best strategy given the risk amount.
@app.route('/Strategy', methods=['POST'])
def Strategy_Out_Page():
    risk = request.values.get('risk')
    try:
        risk = float(risk)
    except:
        risk = 1
    optimal_state = getBestStrategy(portfolioMatrix=port_manager.getPortfolioMatrix(),
                                    risk=risk, budget=3)
    TORREPLACE = buildStrategyHTML(optimal_state,port_manager)
    return render_template("Strategy.html",
                           outPut=True,
                           TORR=TORREPLACE)

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
