import asyncio
import agentpy as ap
from .KQML_message import KQMLMessage
from .KQML_message import *

class Coordinator(ap.Agent):
    def setup(self):
        self.__name = 'Coordinator'
        self.__companies = []
        self.__consumers = []
        self.message_handler = MessageHandler(self.__name, verbose=self.p.verbose)
        self.tasks = []
        self.all_received = False
    
    def check_reception(self):
        return self.all_received

    def register_company(self, company):
        self.__companies.append(company)

    def register_consumer(self, consumer):
        self.__consumers.append(consumer)
    
    def start_process(self):
        # Start threads for companies
        for company in self.__companies:
            thread = threading.Thread(target=company.run)
            thread.start()
            print(f'Company {company.id} thread started.')

        # Start threads for consumers
        for consumer in self.__consumers:
            thread = threading.Thread(target=consumer.run)
            thread.start()
            print(f'Consumer {consumer.id} thread started.')

    def send_msgs2group(self, performative, group, msg_content):
        self.received_counter = len(group)
        for company in group:
            msg = KQMLMessage(performative, self, company.message_handler.name, msg_content)
            self.message_handler.send_message(company.message_handler, msg)

        while self.received_counter > 0:
            self.run()

    def process(self):
        #todo: essas mensagens são bem genéricas, os valores aqui precisam ser decodificados
        self.send_msgs2group('request', self.__companies, 'send_price')
        self.send_msgs2group('inform', self.__consumers, 'offers_available')
        #todo: falta uma última etapa de mensagens do Coordenador para as empresas
        
        while self.received_counter > 0:
            self.run()
            print(f"Messages left to process: {self.received_counter}")
    
    def end(self):
        self.message_handler.stop()
        for company in self.__companies:
            company.message_handler.stop()
        for consumer in self.__consumers:
            consumer.message_handler.stop()

    def run(self):
        while self.message_handler.running:
            message = self.message_handler.receive_message(timeout= 1)
            if message.performative == 'request':
                self.received_counter -=  1
            elif message.performative == 'accept':
                self.received_counter -= 1
            elif message.performative == 'inform':
                self.received_counter -= 1
            if(self.received_counter == 0):
                self.message_handler.running = False
        self.message_handler.running = True
    
    def decode_messages(self):
        #todo: decode messages
        pass

    def process_message(self):
        #todo: after decoding, process each message
        pass