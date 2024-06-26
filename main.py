import matplotlib.pyplot as plt
import numpy as np
from Model.Market import Market
import random

# função de utilidade para consumidores
def consumer_utility_function(company, consumer, information_level) -> float:
    distance = np.linalg.norm(company.position()[0] - consumer.position())
    return company.product_value() - consumer.traveling_cost()*distance - company.price()  # utilidade diminui com maior preço e distância

def company_utility_function(prices, delta) -> float:
    return np.mean(prices) + delta



def main():
    np.random.seed(42)


    INITIAL_SPREAD = 500
    INITIAL_RESERVE = 10000
    INITIAL_OPERATIONAL_COST = 5
    INITIAL_PRICE = 10
    N_CONSUMERS = 100
    N_COMPANIES = 10  # modelo de Hotelling, geralmente 2 empresas

    strategies = np.random.randint(1, 4, N_COMPANIES)
    
    #preço
    #strategies = np.ones((N_COMPANIES))

    #tecnologia
    #strategies = 3*np.ones((N_COMPANIES))

    #informação
    #strategies = 2*np.ones((N_COMPANIES))

    coordinates = np.random.uniform(-1000, 1000, size=(N_COMPANIES + N_CONSUMERS, 2))

    std_dev = 1.0
    companies_cash = abs(np.random.normal(INITIAL_RESERVE, std_dev, N_COMPANIES))
    initial_prices = abs(np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES))
    initial_spreads = abs(np.random.normal(INITIAL_SPREAD, std_dev, N_COMPANIES))
    initial_values = 100*np.ones(N_COMPANIES)



    #monopolio preço
    #companies_cash[1] = 100*INITIAL_RESERVE

    #oligopolio preço
    #companies_cash[0:2] = 100*INITIAL_RESERVE

    #monopolio tecnologia
    #initial_values[1] = 100*initial_values[1]

    #oligopolio tecnologia
    #initial_values[0:5] = 100*initial_values[1]

    #monopolio informação
    #initial_spreads[1] = 100*initial_spreads[1]

    #oligopolio informação
    #initial_spreads[0:2] = 100*initial_spreads[1]
    

    
    

    parameters = {
        'n_consumer_agents': N_CONSUMERS,
        'n_company_agents': N_COMPANIES,
        'coordinates': coordinates,
        'companies_cash': companies_cash,
        'initial_spreads': initial_spreads,
        'initial_prices': initial_prices,
        'strategies': strategies,
        'spread_cost': 10,
        'consumer_utility_function': consumer_utility_function,
        'operational_cost': INITIAL_OPERATIONAL_COST,
        'epsilon': 0.0001,
        'steps': 300,
        'verbose': False,
        'all_values': initial_values,
        'traveling_cost': 0.1,
        'plot': False
    }

    model = Market(parameters)
    results = model.run()
    model.show_results()

if __name__ == "__main__":
    main()
