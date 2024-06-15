import matplotlib.pyplot as plt
import numpy as np
from Model.Market import Market

# função de utilidade para consumidores
def utility_function(company, consumer, information_level) -> float:
    distance = np.linalg.norm(company.position() - consumer.position())
    perceived_price = company.price()
    
    if information_level < 1.0:
        # preços com ruído (informação imperfeita)
        perceived_price += np.random.normal(0, (1 - information_level) * perceived_price)
    
    return -perceived_price - distance  # utilizada diminui com maior preço e distância

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
        'steps': 10
    }

    model = Market(parameters)
    results = model.run()
    model.show_results()

if __name__ == "__main__":
    main()
