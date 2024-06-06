import matplotlib.pyplot as plt
import numpy as np
from Model.Market import Market


def utility_function(company, consumer):
    pass


def main():
    np.random.seed(42)

    INITIAL_PRICE = 0
    N_CONSUMERS = 10
    N_COMPANIES = 10

    # companies cash is defined as a noise around a predefined number
    std_dev = 1.0
    companies_cash = np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES)

    

    parameters = {
        'n_consumer_agents':N_CONSUMERS,
        'n_company_agents':N_COMPANIES,
        'consumer_positions': np.random.rand(N_CONSUMERS, 2) * 100,
        'companies_cash': companies_cash,
        'epsilon': 0.5,
        'steps':10
    }

    model = Market(parameters)
    results = model.run()

if __name__ == "__main__":
    main()