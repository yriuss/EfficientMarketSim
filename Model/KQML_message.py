import threading
import queue
import time 

VERBOSE = True

class KQMLMessage:
    def __init__(self, performative, sender, receiver, content):
        self.performative = performative
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def to_string(self):
        return f'({self.performative} :sender {self.sender.message_handler.name} :receiver {self.receiver} :content {self.content})'

    @staticmethod
    def from_string(message_string):
        parts = message_string.strip('()').split(' :')
        performative = parts[0]
        params = {part.split(' ', 1)[0]: part.split(' ', 1)[1] for part in parts[1:]}
        return KQMLMessage(performative, params['sender'], params['receiver'], params['content'])

class MessageHandler:
    def __init__(self, name, verbose = False):
        self.name = name
        self.inbox = queue.Queue()
        self.running = True
        self.verbose = verbose

    def send_message(self, receiver_handler, message):
        if(self.verbose):
            print(f'{self.name} sending message to {receiver_handler.name}: {message.to_string()}')
        receiver_handler.inbox.put(message)

    def receive_message(self, timeout):
        message = self.inbox.get(timeout=timeout)
        if(self.verbose):
            print(f'{self.name} received message: {message.to_string()}')
        return message
        
        

    def process_message(self, message):
        raise NotImplementedError("This method should be implemented by subclasses")

    def run(self):
        while self.running:
            try:
                message = self.receive_message(timeout = 10)
                self.process_message(message)
            except queue.Empty:
                continue
            

    def stop(self):
        self.running = False