import agentpy as ap
import numpy as np
import asyncio
from Model.KQML_message import MessageHandler, KQMLMessage

class Consumer(ap.Agent):

    def setup(self, positions):
        self.__position = positions[self.id - 1, :]
        self.__leaved = False
        self.information_level = np.random.uniform(0.5, 1.0)  # nível de informação do consumidor
        self.__name = "Consumer" + str(self.id)
        self.message_handler = MessageHandler(self.__name, verbose=False)
        
        self._inbox = asyncio.Queue()

    def name(self):
        return self.__name

    def leaved(self):
        return self.__leaved

    def agent_method(self, utility_values):
        if np.any(utility_values > 0):
            # produto com maior utilidade
            pref_company_index = np.argmax(utility_values)
            self.__pref_company_index = pref_company_index
        else:
            self.leave_market()

    def leave_market(self):
        self.__leaved = True

    def pref_company_id(self):
        return self.__pref_company_index
    
    def position(self):
        return self.__position


    def run(self):
        #todo(ALANA): decide which company is better (decode_msg and process msg are called over here)
        while self.message_handler.running:
            try:
                message = self.message_handler.receive_message(timeout=1)
                if message.performative == 'inform' and message.content == 'offers_available':
                    self.decode_msg(message)
                    self.process_msg(message)
            except Exception as e:
                print(f"Error handling message: {e}")
                continue
    
    def decode_msg(self, message):
    #todo(ALANA): decode received message
        if message.performative == 'inform' and message.content == 'offers_available':
            price_str = message.content.split(':')[1]
            price = float(price_str)
            self.price = price
    def process_msg(self, message):
    #todo(ALANA): process decoded message
        if message.performative == 'inform' and message.content.startswith('price:'):
            utility_values = np.array([self.model.utility_function(company, self, self.information_level) for company in self.model.companies])
            self.agent_method(utility_values)  # Decide qual empresa oferece a maior utilidade esperada
            best_company_id = self.pref_company_id()
            if best_company_id is not None:
                best_company = self.model.companies[best_company_id]
                if self.price <= best_company.price():  # Compra somente se o preço oferecido for menor ou igual ao preço da empresa preferida
                    response = KQMLMessage('accept', self, best_company.message_handler.name, 'buy')
                    self.message_handler.send_message(best_company.message_handler, response)
                else:
                    print(f"Consumer {self.id} received a price offer higher than expected from {message.sender.message_handler.name}. Ignoring offer.")
            else:
                print(f"Consumer {self.id} could not decide on a company to buy from.")
    


 