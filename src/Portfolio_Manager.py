import pandas as pd
import numpy as np
import re

def stringToList(my_string):
    my_string = re.sub(r"[\[\]']", '', my_string)
    # Handle case where there is a space at the end or beginning
    if(my_string[-1] ==" "):
        my_string = my_string[1:]
    if (my_string[-1] == " "):
        my_string = my_string[0:-1]
    my_string = my_string.split(" ")
    for i in range(len(my_string)):
        try:
            my_string[i] = float(my_string[i])
        except:
            pass
    return np.array(my_string)

class PortfolioManager:

    # Constructor
    # Upon initialization read the csv with the current portfolios
    def __init__(self):
        # Get the portfolios as a dataframe
        self.df_ports = pd.read_csv("DataFiles/Portfolios.csv")

        # The lists are stored as strings so we must convert them to lists
        self.numPortfolios = self.df_ports.shape[0]
        for i in self.df_ports.columns:
            for j in range(self.numPortfolios):
                self.df_ports[i][j] = stringToList(self.df_ports[i][j])
                if(i == "weights" and sum(self.df_ports[i][j])-1 > 10**-6):
                    self.df_ports[i][j] = self.df_ports[i][j]/sum(self.df_ports[i][j])

        # Get the stock info dataframe
        self.df_stocks = pd.read_csv("DataFiles/StockInfo.csv")

    # Add a new portfolio to the current set
    def addPortfolio(self,listOfTickers,weights):
        # Convert lists and normalize weights
        listOfTickers = np.array(listOfTickers)
        weights = np.array(weights)
        weights = weights/sum(weights)
        if(sum(weights)-1 > 10**-6):
            # TODO : remove this
            raise ValueError("STOPPPP!!!")

        # Increment number of portfolios and add new row
        self.numPortfolios +=1
        self.df_ports.loc[self.numPortfolios] = [listOfTickers,weights]

        # Save the data
        self.df_ports.to_csv("DataFiles/Portfolios.csv",index=False)

    # Get the matrix representation of the set of portfolios
    def getPortfolioMatrix(self):
        numStocks = self.df_stocks.shape[0]
        A = np.zeros((numStocks,self.numPortfolios))

        for port_index in range(self.numPortfolios):
            port_stocks = self.df_ports['list_of_stocks'][port_index]
            port_weights = self.df_ports['weights'][port_index]
            for i in range(len(port_weights)):
                index_list = self.df_stocks.index[self.df_stocks['Symbol'] == port_stocks[i]].tolist()
                if len(index_list) != 1:
                    raise ValueError("STOPPPP 222!!!")
                stock_index = index_list[0]
                A[stock_index,port_index] = port_weights[i]

        return A


# TEMP DEBUGGING
# todo: remove this
if __name__ == "__main__":
    m = PortfolioManager()
    port_stocks = ["IRM","HD","FOX","BLL"]
    port_weights = [1,2,.5,1]
    # m.addPortfolio(port_stocks,port_weights)
    A = m.getPortfolioMatrix()
    print(A.shape)
    print(np.sum(A, axis=0))