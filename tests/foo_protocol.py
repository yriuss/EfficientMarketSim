from Model.Company import Company
from Model. Consumer import Consumer
from Model.Coordinator import Coordinator
import numpy as np
import agentpy as ap

class DummyMarket(ap.Model):
    def setup(self):
        """ Inicializa uma lista de novos agentes. """
        self.consumers = ap.AgentList(self, self.p.n_consumer_agents, Consumer, positions=self.p.consumer_positions)
        self.companies = ap.AgentList(self, self.p.n_company_agents, Company)
        self.coordinator = ap.AgentList(self, 1, Coordinator)

        for consumer in self.consumers:
            self.coordinator.register_consumer(consumer)
    
        for company in self.companies:
            self.coordinator.register_company(company)

        self.coordinator.start_process()

    def step(self):
        self.coordinator.process()

    def update(self):
        pass
        
    def end(self):
        self.coordinator.end()

def dummy(company, consumer, information_level) -> float:
    
    return -123123

VERBOSE = True


def main():
    
    
    INITIAL_PRICE = 0
    N_CONSUMERS = 5000
    N_COMPANIES = 500

    std_dev = 1.0
    companies_cash = np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES)
    initial_prices = np.random.normal(INITIAL_PRICE, std_dev, N_COMPANIES)

    parameters = {
        'n_consumer_agents': N_CONSUMERS,
        'n_company_agents': N_COMPANIES,
        'consumer_positions': np.random.rand(N_CONSUMERS, 2) * 100,
        'companies_cash': companies_cash,
        'initial_prices': initial_prices,
        'utility_function': dummy,
        'epsilon': 0.5,
        'steps': 1,
        'verbose': True
    }
    model = DummyMarket(parameters)
    results = model.run()

if __name__ == '__main__':
    main()
