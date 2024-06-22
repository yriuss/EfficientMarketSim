import agentpy as ap
import numpy as np
import asyncio
import traceback
from Model.KQML_message import MessageHandler, KQMLMessage


class Company(ap.Agent):

    def setup(self):
        self.__epsilon = self.p.epsilon
        self.__position = np.random.rand(1, 2) * 100
        self.__cash = self.p.companies_cash[self.id - self.p.n_consumer_agents - 1]
        self.__price = self.p.initial_prices[self.id - self.p.n_consumer_agents - 1]
        self.__prices = self.p.initial_prices
        self.__strategy = 'random'  # estratégia (acho que seria melhor diferentes estratégias serem aleatoriamente distribuídas ao invés de determinar uma estratégia aleatória para uma única empresa, mas de início pode ser uma única estratégia mais simples possível e depois discutimos)
        self.__operational_cost = self.p.operational_cost
        self.information_level = np.random.uniform(0.5, 1.0)  # nível de informação da empresa
        self.__name = "Company" + str(self.id)
        self.message_handler = MessageHandler(self.__name, verbose=self.p.verbose)
        
        self._inbox = asyncio.Queue()

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

    def evaluate_change_in_price(self):
        # decisão da empresa sobre os preços
        if(self.__price >= np.mean(self.__prices)):
            self.__price -= self.__epsilon
        
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
