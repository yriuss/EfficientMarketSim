import agentpy as ap
import numpy as np
import asyncio
import traceback
from Model.KQML_message import MessageHandler, KQMLMessage


class Company(ap.Agent):

    def setup(self):
        self.__epsilon = self.p.epsilon
        self.__position = self.p.coordinates[self.id -1 ,:]
        self.__cash = self.p.companies_cash[self.id - self.p.n_consumer_agents - 1]
        self.__price = self.p.initial_prices[self.id - self.p.n_consumer_agents - 1]
        self.__prices = self.p.initial_prices
        self.__strategy = self.model.p.strategies[self.id - self.p.n_consumer_agents - 1]
        self.__operational_cost = self.p.operational_cost
        self.information_level = np.random.uniform(0.5, 1.0)  # nível de informação da empresa
        self.__name = "Company" + str(self.id)
        self.__max_spread_thresh = self.model.p.initial_spreads[self.id - self.p.n_consumer_agents - 1]
        self.message_handler = MessageHandler(self.__name, verbose=self.p.verbose)
        self.__product_value = self.model.p.all_values[self.id - self.p.n_consumer_agents - 1]
        self._inbox = asyncio.Queue()
    
    def max_spread_thresh(self):
        return self.__max_spread_thresh

    def product_value(self):
        return self.__product_value

    def strategy(self):
        return self.__strategy

    def strategy1(self):
        if(self.__price > np.mean(self.__prices)):
            self.__price -= self.__epsilon
    
    def strategy2(self):
        if(self.__cash > 0):
            self.__max_spread_thresh += self.__epsilon
            self.__cash -= self.p.spread_cost
    
    def strategy3(self):
        if(self.__price > self.__operational_cost):
            self.__product_value += self.__epsilon
            self.__operational_cost += self.__epsilon

    def name(self):
        return self.__name

    def position(self):
        return self.__position

    def price(self):
        return self.__price

    def cash(self):
        return self.__cash
    
    def get_prices_info(self, prices):
        self.__prices = prices

    def define_strategy(self):
        # decisão da empresa sobre os preços
        if(self.__strategy == 1):
            self.strategy1()
        elif(self.__strategy == 2):
            self.strategy2()
        elif(self.__strategy == 3):
            self.strategy3()
        
    def sell(self, n_sellings):
        self.__cash += self.calculate_profit(n_sellings*self.__price)
    
    def calculate_profit(self, earnings):
        return earnings - self.__operational_cost

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
    
    def run(self):
        while self.message_handler.running:
            try:
                message = self.message_handler.receive_message(timeout=1)
                if message and 'Company' in message.receiver:
                    if(self.p.verbose):
                        print(f'Company {self.id} received message: {message.to_string()}')

                    if message.performative == 'request' and message.content == 'send_price':
                        self.decode_msg(message)
                    else:
                        self.process_msg(message)
                else:
                    print(f'Company {self.id} did not receive any message.')

            except Exception as e:
                continue
            
    def decode_msg(self, message):
        #todo(ALANA): decode received message
        if message.performative == 'request' and message.content == 'send_price':
            price = self.price()  # Utilize o preço da empresa
            response = KQMLMessage('inform', self, message.sender.message_handler.name, f'price:{price}')
            #print(f'Company {self.id} sending price: {price}')
            self.message_handler.send_message(message.sender.message_handler, response)
        else:
            print(f"Company {self.id} received unknown message: {message}")

    def process_msg(self, message):
        #todo(ALANA)
        if message.performative == 'inform' and 'price:' in message.content:
            print(f"Company {self.id} received price information: {message.content.split(':')[1]}")
        else:
            print(f"Company {self.id} received unknown message in process_msg: {message}")
