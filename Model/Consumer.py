import agentpy as ap
import numpy as np

class Consumer(ap.Agent):

    def setup(self, position):
        self.position = position

    def agent_method(self, utility_values):
        if np.any(utility_values > 0):
            # chose the product with max utility
            product = max(utility_values)
        else:
            self.leave_market()
    def leave_market(self):
        pass