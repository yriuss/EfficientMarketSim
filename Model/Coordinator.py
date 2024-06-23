import asyncio
import agentpy as ap
from .KQML_message import KQMLMessage
from .KQML_message import *
import numpy as np

class Coordinator(ap.Agent):
    def setup(self):
        self.__name = 'Coordinator'
        self.__companies = []
        self.__consumers = []
        self.message_handler = MessageHandler(self.__name, verbose=self.p.verbose)
        self.tasks = []
        self.all_received = False
        self.__offers = []
    
    def consumers(self):
        return self.__consumers

    def check_reception(self):
        return self.all_received

    def register_company(self, company):
        self.__companies.append(company)
    
    def remove_company(self, idx):
        del self.__companies[idx]
    
    def remove_consumer(self, idx):
        del self.__consumers[idx]

    def register_consumer(self, consumer):
        self.__consumers.append(consumer)
    
    def start_process(self):
        # Start threads for companies
        for company in self.__companies:
            thread = threading.Thread(target=company.run)
            thread.start()

        # Start threads for consumers
        for consumer in self.__consumers:
            thread = threading.Thread(target=consumer.run)
            thread.start()

    def send_msgs2group(self, performative, group, msg_content):
        self.received_counter = len(group)
        for company in group:
            msg = KQMLMessage(performative, self, company.message_handler.name, msg_content)
            self.message_handler.send_message(company.message_handler, msg)

        while self.received_counter > 0:
            self.run()

    def process(self):
        #todo: essas mensagens são bem genéricas, os valores aqui precisam ser decodificados
        if(self.__companies != []):
            self.send_msgs2group('request', self.__companies, 'send_price')

        
        for consumer in self.__consumers:
            offers = []
            for i, company in enumerate(self.__companies):
                if(np.linalg.norm(company.position() - consumer.position()) <= company.max_spread_thresh()):
                    offers.append(self.__offers[i])
            self.send_msgs2group('inform', [consumer], 'offers:'+str(offers))
        
        for i, company in enumerate(self.__companies):
            consumers_that_bought = 0
            for consumer in self.__consumers:
                if(consumer.bought(company.name())):
                    consumers_that_bought += 1
            company.sell(consumers_that_bought)

            # se o caixa da empresa atingir 0, ela declara falência
            if(company.cash() <= 0):
                company.message_handler.stop()
                del self.__companies[i]
            else:
                company.get_prices_info(self.__offers)
                company.define_strategy()

        self.__offers = []
        #todo: falta uma última etapa de mensagens do Coordenador para as empresas

    
    def end(self):
        self.message_handler.stop()
        for company in self.__companies:
            company.message_handler.stop()
        for consumer in self.__consumers:
            consumer.message_handler.stop()

        

    def run(self):
        while self.message_handler.running:
            try:
                message = self.message_handler.receive_message(timeout= 1)
                message = self.decode_messages(message)
            except Exception as e:
                continue
        self.message_handler.running = True
    



    def decode_messages(self, message):
        if message.performative == 'request':
            self.received_counter -=  1
        elif message.performative == 'accept':
            self.received_counter -= 1
        elif message.performative == 'inform':
            self.received_counter -= 1

            if "Company" in message.sender.name():
                self.__offers.append(float(message.content.split(':')[1]))
        elif message.performative == 'reject':
            self.received_counter -= 1
            for i, consumer in enumerate(self.__consumers):
                if(consumer.name() == message.sender.name()):
                    consumer.message_handler.stop()
                    del self.__consumers[i]
                    break
        if(self.received_counter == 0):
            self.message_handler.running = False
        
        return message

    def process_message(self):
        #todo: after decoding, process each message
        pass