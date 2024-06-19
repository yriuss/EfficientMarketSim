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
        print(f'Company {company.id} registered.')

    def register_consumer(self, consumer):
        self.__consumers.append(consumer)
        print(f'Consumer {consumer.id} registered.')

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
        for recipient in group:
            msg = KQMLMessage(performative, self, recipient.message_handler.name, msg_content)
            print(f'{msg}')
            self.message_handler.send_message(recipient.message_handler, msg)
            print(f'Sent {performative} message to {recipient.__class__.__name__} {recipient.id} with content: {msg_content}')

        while self.received_counter > 0:
            time.sleep(1)  # Aguarda um segundo para evitar alta utilização de CPU

    def process(self):
        print("Coordinator processing messages")
        #todo: essas mensagens são bem genéricas, os valores aqui precisam ser decodificados
        self.send_msgs2group('request', self.__companies, 'send_price')
        self.send_msgs2group('inform', self.__consumers, 'offers_available')
        #todo: falta uma última etapa de mensagens do Coordenador para as empresas
        print("Messages sent to all companies and consumers")

    
    def end(self):
        self.message_handler.stop()
        for company in self.__companies:
            company.message_handler.stop()
        for consumer in self.__consumers:
            consumer.message_handler.stop()

    def run(self):
        while self.message_handler.running:
            try:
                message = self.message_handler.receive_message(timeout=1)
                if message is not None:
                    if message.performative == 'request':
                        self.received_counter -=  1
                    elif message.performative == 'accept':
                        self.received_counter -= 1
                    elif message.performative == 'inform':
                        self.received_counter -= 1

                    if self.received_counter == 0:
                        self.message_handler.running = False
                else:
                    print(f'{self.__name} did not receive any message.')
                
            except Exception as e:
                print(f"Error handling message in {self.__name}: {str(e)}")
                import traceback
                print(traceback.format_exc())
                continue
    
    def decode_messages(self):
        #todo: decode messages
        pass

    def process_message(self):
        #todo: after decoding, process each message
        pass