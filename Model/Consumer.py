import agentpy as ap
import numpy as np
import asyncio
from Model.KQML_message import MessageHandler, KQMLMessage

class Consumer(ap.Agent):

    def setup(self):
        self.__position = self.p.coordinates[self.id - 1,:]
        self.__leaved = False
        self.information_level = np.random.uniform(0.5, 1.0)  # nível de informação do consumidor
        self.__name = "Consumer" + str(self.id)
        self.message_handler = MessageHandler(self.__name, verbose=False)
        
        self._inbox = asyncio.Queue()
        
        self.__traveling_cost = self.model.p.traveling_cost
        self.__buy = False
        self.__pref_company_index = None
        self.__bought_from = None

    def bought(self, company):
        if(self.__buy and company == self.__bought_from):
            self.__bought_from = None
            self.__buy = False
            return True
        else:
            return False

    
    def traveling_cost(self):
        return self.__traveling_cost
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
                if message.performative == 'inform' and message.content.startswith('offers'):
                    decoded_msg = self.decode_msg(message)
                    self.process_msg(decoded_msg)
            except Exception as e:
                #print(f"Error handling message: {e}")
                continue
    
    def decode_msg(self, message):
    #todo(ALANA): decode received message
        if message.performative == 'inform' and message.content.startswith('offers'):
            string_elements = message.content.strip(('offers:[]')).split(',')
            if(string_elements[0] != ''):
                message.content = [float(element) for element in string_elements]
            else:
                message.content = []

        return message

    def process_msg(self, message):
    #todo(ALANA): process decoded message
        if message.performative == 'inform' and type(message.content) == list:
            if(message.content!= []):
                utility_values = np.array([self.model.p.consumer_utility_function(company, self, self.information_level) for company in self.model.companies])
                self.__pref_company_id = None
                self.agent_method(utility_values)  # Decide qual empresa oferece a maior utilidade esperada
                best_company_id = self.pref_company_id()
                if best_company_id is not None:
                    best_company = self.model.companies[best_company_id]

                    response = KQMLMessage('accept', self, self.model.coordinator.message_handler.name[0], 'buy')
                    self.message_handler.send_message(self.model.coordinator.message_handler, response)
                    self.__buy = True
                    self.__bought_from = best_company.name()
                else:
                    response = KQMLMessage('reject', self, self.model.coordinator.message_handler.name[0], 'leave')
                    self.message_handler.send_message(self.model.coordinator.message_handler, response)
                    print(f"Consumer {self.id} is leaving the market.")
                    self.__buy = False
            else:
                #self.leave_market()
                response = KQMLMessage('reject', self, self.model.coordinator.message_handler.name[0], 'wait')
                self.message_handler.send_message(self.model.coordinator.message_handler, response)
                #print(f"Consumer {self.id} is leaving the market.")
                self.__buy = False
    


 