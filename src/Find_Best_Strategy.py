from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.aqua.components.optimizers import COBYLA
from qiskit.aqua.algorithms import QAOA
from qiskit.aqua import QuantumInstance
from qiskit import Aer
import pandas as pd
import numpy as np
from Portfolio_Manager import PortfolioManager
from Edited_Qiskit_portfolio import *


def getBestStrategy(portfolioMatrix,risk,budget,penalty):
    # Set seed for reproducable results
    seed = 503678

    # Get the moments of the stocks
    df_Prices = pd.read_csv("DataFiles/StockPrices.csv")
    mu = np.array(df_Prices.mean())
    sigma = np.array(df_Prices.cov())

    # Set up the Quantum operator for a financial portfolio
    qubitOperator, offset = get_operator(mu, sigma, risk, portfolioMatrix, budget, penalty)

    # Set backend. We are considering pure states
    # so Aer's state vector simulator will work best
    backend = Aer.get_backend('statevector_simulator')

    # Set up optimization
    cobyla = COBYLA() # Constrained Optimization By Linear Approximation optimizer.
    cobyla.set_options(maxiter=250)
    qaoa = QAOA(qubitOperator, cobyla, 3) # Quantum Approximate Optimization Algorithm
    qaoa.random_seed = seed
    quantum_instance = QuantumInstance(backend=backend, seed_simulator=seed, seed_transpiler=seed)

    # Run optimization
    result = qaoa.run(quantum_instance)

    # Parse Results
    op_State = sample_most_likely(result.eigenstate)
    op_Cost = portfolio_value(op_State, mu, sigma, risk, portfolioMatrix, budget, penalty)
    op_Return = portfolio_expected_value(op_State, mu, portfolioMatrix)
    op_Risk = portfolio_variance(op_State, sigma, portfolioMatrix)

    return [op_State,op_Cost,op_Return,op_Risk]

# todo : get rid of this
if __name__ == "__main__":

    # Get portfolio matrix
    port_manager = PortfolioManager()
    portfolioMatrix = port_manager.getPortfolioMatrix()

    results = getBestStrategy(portfolioMatrix=portfolioMatrix,risk=.5,budget=3,penalty=2)
    print("Nice")
