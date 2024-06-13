import agentpy as ap
import numpy as np

class Company(ap.Agent):

    def setup(self):
        self.__epsilon = self.p.epsilon
        self.__position = np.random.rand(1, 2) * 100
        self.__cash = self.p.companies_cash[self.id - self.p.n_consumer_agents - 1]
        self.__prices = self.p.initial_prices[self.id - self.p.n_consumer_agents - 1]
        self.__strategy = 'random'  # estratégia
        self.information_level = np.random.uniform(0.5, 1.0)  # nível de informação da empresa

    def position(self):
        return self.__position

    def price(self):
        return self.__prices

    def cash(self):
        return self.__cash

    def evaluate_change_in_price(self):
        # decisão da empresa sobre os preços
        best_price = self.__prices
        best_profit = self.calculate_profit(self.__prices)

        for i in [-self.__epsilon, 0, self.__epsilon]:
            new_price = self.__prices + i
            new_profit = self.calculate_profit(new_price)
            if new_profit > best_profit:
                best_profit = new_profit
                best_price = new_price
        
        self.__prices = best_price

    def calculate_profit(self, price):
        # lucro com base no preço
        total_utility = 0
        for consumer in self.model.consumers:
            utility = utility_function(self, consumer, self.information_level)
            if utility > 0:
                total_utility += utility
        return total_utility - price

    def record(self, variable, value):
        if not hasattr(self, '_records'):
            self._records = {}
        if variable not in self._records:
            self._records[variable] = []
        self._records[variable].append(value)

    def recorded(self, variable):
        if hasattr(self, '_records') and variable in self._records:
            return self._records[variable]
        return []
