import matplotlib.pyplot as plt
import numpy as np
from Model.Market import Market
from Model.utility import utility_function 

def main():
    np.random.seed(42)

    INITIAL_PRICE = 0
    N_CONSUMERS = 10
    N_COMPANIES = 2  # modelo de Hotelling, geralmente 2 empresas

    std_dev = 1.0
    companies_cash = np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES)
    initial_prices = np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES)

    parameters = {
        'n_consumer_agents': N_CONSUMERS,
        'n_company_agents': N_COMPANIES,
        'consumer_positions': np.random.rand(N_CONSUMERS, 2) * 100,
        'companies_cash': companies_cash,
        'initial_prices': initial_prices,
        'utility_function': utility_function,
        'epsilon': 0.5,
        'steps': 10,
        'verbose': True
    }

    model = Market(parameters)
    results = model.run()
    model.show_results()

if __name__ == "__main__":
    main()
