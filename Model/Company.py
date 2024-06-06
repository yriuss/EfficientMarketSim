import agentpy as ap
import numpy as np

class Company(ap.Agent):

    def setup(self):
        self.__epsilon = self.p.epsilon
        #todo: company choses best positions to be in
        self.__position = np.random.rand(1, 2) * 100
        self.__cash = self.p.companies_cash[self.id - self.p.n_consumer_agents - 1]
        self.__prices = self.p.initial_prices[self.id - self.p.n_consumer_agents - 1]

    def position(self):
        return self.__position

    def evaluate_change_in_price(self):
        #todo: company should decide if its prices are going to change
        for i in [-self.__epsilon, 0, self.__epsilon]:
            pass