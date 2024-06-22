import matplotlib.pyplot as plt
import numpy as np
from Model.Market import Market

# função de utilidade para consumidores
def consumer_utility_function(company, consumer, information_level) -> float:
    distance = np.linalg.norm(company.position()[0] - consumer.position())
    return consumer.value() - consumer.traveling_cost()*distance - company.price()  # utilidade diminui com maior preço e distância

def company_utility_function(prices, delta) -> float:
    return np.mean(prices) + delta



def main():
    np.random.seed(42)

    INITIAL_PRICE = 0
    N_CONSUMERS = 50
    N_COMPANIES = 2  # modelo de Hotelling, geralmente 2 empresas

    std_dev = 1.0
    companies_cash = 10000*abs(np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES))
    initial_prices = 100*abs(np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES))

    parameters = {
        'n_consumer_agents': N_CONSUMERS,
        'n_company_agents': N_COMPANIES,
        'consumer_positions': np.random.rand(N_CONSUMERS, 2) * 100,
        'companies_cash': companies_cash,
        'initial_prices': initial_prices,
        'consumer_utility_function': consumer_utility_function,
        'operational_cost': 100,
        'epsilon': 0.5,
        'steps': 300,
        'verbose': True,
        'value': 100,
        'traveling_cost': 0.1
    }

    model = Market(parameters)
    results = model.run()
    model.show_results()

if __name__ == "__main__":
    main()
