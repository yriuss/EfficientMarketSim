import agentpy as ap

class MyAgent(ap.Agent):

    def setup(self):
        # Initialize an attribute with a parameter
        self.my_attribute = self.p.my_parameter

    def agent_method(self):
        # Define custom actions here
        pass