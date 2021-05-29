from qiskit.finance.data_providers import RandomDataProvider
import datetime
import pandas as pd

# This script generates fake stock data for all the companies currently in the S&P 500.
def run():
    # Get a current list of companies in the S&P 500 from wikipedia
    df_Info = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

    # Get number of companiesin S&P 500
    numStocks = df_Info.shape[0]

    # Generate data using Qiskit's financial data provider
    stocks = [("TICKER%s" % i) for i in range(numStocks)]
    Qiskit_Data = RandomDataProvider(tickers=stocks,
                     start=datetime.datetime(2021,4,28),
                     end=datetime.datetime(2021,5,29))
    Qiskit_Data.run()

    # Get the data as a dataframe
    df_Prices = pd.DataFrame(Qiskit_Data._data).T

    # Set the columns names
    df_Prices.columns = df_Info['Symbol']

    # Output data frames to csv files
    df_Prices.to_csv("DataFiles/StockPrices.csv",index=False)
    df_Info.to_csv("DataFiles/StockInfo.csv",index=False)

    # Print results
    print("Successfully generated data for "+str(numStocks) +" companies.")

if __name__ == "__main__":
    run()
