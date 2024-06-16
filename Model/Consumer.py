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
                print(f'1')
                if message.performative == 'inform' and message.content == 'offers_available':
                    self.decode_msg(message)  # Decodifica a mensagem e responde com 'accept'
                else:
                    self.process_msg(message)  # Processa outras mensagens recebidas
            except Exception as e:
                print(f"Error handling message: {e}")
                continue
    
    def decode_msg(self, message):
    #todo(ALANA): decode received message
        if message.performative == 'inform' and message.content == 'offers_available':
            # apenas respondendo com 'accept' para a primeira empresa
            company_id = self.model.coordinator.get_company_for_consumer(self)
            company = self.model.companies[company_id]
            response = KQMLMessage('accept', self, company.message_handler.name, 'buy')
            self.message_handler.send_message(company.message_handler, response)
        else:
            print(f"Consumer {self.id} received unknown message: {message}")

    def process_msg(self, message):
    #todo(ALANA): process decoded message
        if message.performative == 'accept' and message.content == 'buy':
            print(f"Consumer {self.id} received confirmation of purchase from {message.sender.name}")
        else:
            print(f"Consumer {self.id} received unknown message in process_msg: {message}")

    